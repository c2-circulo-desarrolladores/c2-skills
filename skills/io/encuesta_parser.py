import re
from pathlib import Path

import polars as pl

from skills.conf import MIEMBROS


def obtener_encuestas(nombre_encuesta: str) -> list[Path]:
    encuestas_paths: list[Path] = []
    for carpeta_miembro in MIEMBROS.iterdir():
        encontrado = False
        for archivo in carpeta_miembro.iterdir():
            if archivo.name.lower() == nombre_encuesta.lower():
                encuestas_paths.append(archivo)
                encontrado = True
                break
        if not encontrado:
            # raise FileNotFoundError(
            #     f"El miembro '{carpeta_miembro.name.title()}' no tiene la encuesta {nombre_encuesta}"
            # )
            continue

    if not encuestas_paths:
        raise FileNotFoundError(
            f"No se encontraron encuestas de nombre '{nombre_encuesta}'"
        )
    return encuestas_paths


def parsear_encuesta(encuesta_path: Path):
    with open(encuesta_path, mode="r", encoding="utf-8") as f:
        encuesta_str = f.read()

    encuesta_core = encuesta_str.split("| 3 | Avanzado |")[-1]
    cuadricula = []
    nivel_0: str = encuesta_path.parent.name
    nivel_1: str = ""
    nivel_2: str = ""
    for idx, linea in enumerate(encuesta_core.splitlines()):
        linea = linea.strip()

        if not linea or linea in ("| Tema | Conceptos | Valor |", "|---|---|---|"):
            continue

        m = re.match(r"^## (.+)$", linea)
        if m:
            nivel_1 = m.group(1).strip()
            continue

        m = re.match(r"^### (.+)$", linea)
        if m:
            nivel_2 = m.group(1).strip()
            continue

        if linea.startswith("|") and linea.endswith("|"):
            valor, tema, conceptos = [v.strip() for v in linea[1:-1].split("|")]
            if not valor:
                valor_limpio = 0
            else:
                valor_limpio = int(valor.strip())
            if valor_limpio not in (0, 1, 2, 3):
                print(valor_limpio)
                raise ValueError(
                    f"Error en la línea {idx} de {encuesta_path}: No se colocó como valor un número del 0-3\nLínea: {linea}"
                )
            cuadricula.append((nivel_0, nivel_1, nivel_2, tema, conceptos, int(valor_limpio)))
        else:
            raise ValueError(
                f"Error en la línea {idx} de {encuesta_path}: No cumple ningún patrón\nLínea: {linea}",
            )
    return pl.DataFrame(
        data=cuadricula,
        schema={
            "miembro": pl.String,
            "tema": pl.String,
            "conceptos": pl.String,
            "seccion": pl.String,
            "encuesta": pl.String,
            "valor": pl.Int8,
        },
        orient="row",
    )


def main()-> pl.DataFrame:
    lista_encuestas = obtener_encuestas("FUNDAMENTALS.md")
    lista_dataframes: list[pl.DataFrame] = []
    for encuesta_path in lista_encuestas:
        lista_dataframes.append(parsear_encuesta(encuesta_path))

    return pl.concat(lista_dataframes)


if __name__ == "__main__":
    main()
