from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import polars as pl
from jinja2 import Environment, FileSystemLoader

from skills.conf import ENCUESTAS_FINALES, JINJA_TEMPLATES, SOURCES


class JinjaRenderer(ABC):
    source_file: Path
    template_name: str
    source_schema: dict[str, Any]

    def _read_source(self) -> pl.DataFrame:
        return pl.read_excel(
            self.source_file, engine="calamine", schema_overrides=self.source_schema
        )

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
    source_file = SOURCES / "fundamentals.xlsx"
    source_schema = {
        "tema": pl.String,
        "conceptos": pl.String,
        "seccion": pl.String,
        "encuesta": pl.String,
    }
    template_name = "fundamentals.md.jinja2"

    def _aggregate(self, df: pl.DataFrame) -> pl.DataFrame:
        return (
            df.group_by(["encuesta", "seccion"], maintain_order=True)
            .agg(pl.struct(["tema", "conceptos"]).alias("temas"))
            .group_by("encuesta", maintain_order=True)
            .agg(pl.struct(["seccion", "temas"]).alias("secciones"))
        )


def main():
    FundamentalsRenderer().save_rendered(ENCUESTAS_FINALES / "fundamentals_template.md")


if __name__ == "__main__":
    main()
