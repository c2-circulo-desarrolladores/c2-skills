import polars as pl
import streamlit as st

from skills.app.shared.figures import create_bar_chart


def seleccionar_y_filtrar(
    df: pl.DataFrame, columna: str, label: str, key: str
) -> pl.DataFrame:
    """
    A partir de un dataframe, genera un selectbox con los datos únicos
    de una columna y devuelve el df filtrado.
    """
    opciones = (
        df.select(pl.col(columna).unique(maintain_order=True))
        .to_series()
        .sort(descending=True)
        .to_list()
    )
    seleccion = st.selectbox(label, opciones, format_func=str.capitalize, key=key)
    return df.filter(pl.col(columna) == seleccion)



def calcular_progreso(df: pl.DataFrame, group_col: str) -> str:
    """Calcula el progreso promedio (0-100%) agrupando por `group_col`."""
    promedio = (
        df.group_by([group_col], maintain_order=True)
        .agg(pl.col("valor").mean())
        .mean()
        .select(pl.col("valor"))
        .item()
    )
    return f"{round(promedio / 3 * 100, ndigits=2)}%"


def agrupar_por_tema(tema_df: pl.DataFrame) -> pl.DataFrame:
    """Agrupa por tema y sección, promediando el valor."""
    return tema_df.group_by(["tema", "seccion"], maintain_order=True).agg(
        pl.col("valor").mean()
    )


def render_bar_charts(
    tema_grouped: pl.DataFrame, col1, col2, reverse: bool = True
) -> None:
    """Renderiza un bar chart por cada tema, alternando entre columnas."""
    temas = tema_grouped["tema"].unique(maintain_order=True).to_list()

    for idx, tema in enumerate(temas):
        tema_filtrado = tema_grouped.filter(pl.col("tema") == tema)
        if reverse:
            tema_filtrado = tema_filtrado.reverse()

        columna = col2 if idx % 2 else col1
        with columna:
            create_bar_chart(tema_filtrado, tema, idx)