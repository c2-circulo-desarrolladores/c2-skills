import polars as pl
from pathlib import Path
from dashboard.conf import MIEMBROS


def obtener_encuestas(nombre_encuesta: str) -> list[Path]:
    encuestas_paths = [
        archivo
        for carpeta_miembro in MIEMBROS.iterdir()
        for archivo in carpeta_miembro.iterdir()
        if archivo.name == nombre_encuesta
    ]
    if not encuestas_paths:
        raise FileNotFoundError(f"No se encontraron encuestas de nombre '{nombre_encuesta}'")
    return encuestas_paths


print(obtener_encuestas("FUNDAMENTALS.md"))
