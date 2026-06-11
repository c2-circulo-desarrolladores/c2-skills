from pathlib import Path
from typing import Any

import polars as pl

from skills.conf import SOURCES, JINJA_TEMPLATES
from jinja2 import Environment, FileSystemLoader
from abc import ABC, abstractmethod


class JinjaRenderer(ABC):
    source_file: Path
    template_name: str
    source_schema: dict[str, Any]

    def _read_source(self) -> pl.DataFrame:
        return pl.read_excel(
            self.source_file, engine="calamine", schema_overrides=self.source_schema
        )

    @abstractmethod
    def _aggregate(self, df: pl.DataFrame) -> list[dict]: ...

    def _render(self, data: list[dict]) -> str:
        env = Environment(loader=FileSystemLoader(JINJA_TEMPLATES))
        return env.get_template(self.template_name).render(data=data)

    def run(self) -> str:
        df = self._read_source()
        data = self._aggregate(df)
        return self._render(data)


class FundamentalsRenderer(JinjaRenderer):
    source_file = SOURCES / "fundamentals.xlsx"
    source_schema = {
        "tema": pl.String,
        "conceptos": pl.String,
        "seccion": pl.String,
        "encuesta": pl.String,
    }
    template_name = "fundamentals.md.jinja2"

    def _aggregate(self, df: pl.DataFrame) -> list[dict]:
        return (
            df.group_by(["encuesta", "seccion"], maintain_order=True)
            .agg()
            .group_by("encuesta", maintain_order=True)
            .agg(pl.col("seccion"))
            .to_dicts()
        )


def main():
    print(FundamentalsRenderer().run())


main()
