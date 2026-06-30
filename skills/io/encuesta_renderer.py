from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import polars as pl
from jinja2 import Environment, FileSystemLoader
import yaml

from skills.conf import ENCUESTAS_FINALES, JINJA_TEMPLATES, SOURCES


class JinjaRenderer(ABC):
    source_file: Path
    template_name: str
    source_schema: dict[str, Any]

    def _read_source(self) -> pl.DataFrame: ...

    @abstractmethod
    def _aggregate(self, df: pl.DataFrame) -> pl.DataFrame: ...

    def _render(self, data: list[dict]) -> str:
        env = Environment(loader=FileSystemLoader(JINJA_TEMPLATES))
        return env.get_template(self.template_name).render(data=data)

    def save_rendered(self, output_path: Path) -> None:
        df = self._read_source()
        data = self._aggregate(df)
        # print(data)
        with open(output_path, mode="w", encoding="utf-8") as f:
            f.write(self._render(data.to_dicts()))
        print(f"{self.source_file.name} rendered and saved to {output_path}")


class FundamentalsRenderer(JinjaRenderer):
    source_file = SOURCES / "fundamentals.yml"
    source_schema = {
        "tema": pl.String,
        "conceptos": pl.String,
        "seccion": pl.String,
        "encuesta": pl.String,
    }
    template_name = "fundamentals.md.jinja2"

    def _read_source(self) -> pl.DataFrame:
        with open(self.source_file, mode="r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        rows = []
        for encuesta, secciones in raw["curriculum"].items():
            for seccion, temas in secciones.items():
                for item in temas:
                    rows.append(
                        {
                            "encuesta": encuesta,
                            "seccion": seccion,
                            "tema": item["tema"],
                            "conceptos": ", ".join(item["conceptos"]),  # flatten list → str
                        }
                    )

        return pl.DataFrame(rows, schema=self.source_schema)

    def _aggregate(self, df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.group_by(["encuesta", "seccion"], maintain_order=True)
            .agg(pl.struct(["tema", "conceptos"]).alias("temas"))
            .group_by("encuesta", maintain_order=True)
            .agg(pl.struct(["seccion", "temas"]).alias("secciones"))
        )


def main():
    FundamentalsRenderer().save_rendered(ENCUESTAS_FINALES / "fundamentals.md")


if __name__ == "__main__":
    main()
