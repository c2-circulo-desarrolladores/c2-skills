import polars as pl
from dashboard.conf import ROOT


def main():
    schema = {
        "name": pl.String,
        "description": pl.String,
        "analysis": pl.UInt8,
        "science": pl.UInt8,
        "engineering": pl.UInt8,
        "ai": pl.UInt8,
        "automation": pl.UInt8,
    }

    return pl.read_excel(
        ROOT / "data" / "library_skills.xlsx",
        schema_overrides=schema,
        columns=list(schema.keys()),
    )


if __name__ == "__main__":
    print(main())
