import polars as pl
import streamlit as st


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
