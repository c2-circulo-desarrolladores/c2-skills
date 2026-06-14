import plotly.express as px
import polars as pl
import streamlit as st


def seleccionar_y_filtrar(
    df: pl.DataFrame, columna: str, label: str, key: str
) -> pl.DataFrame:
    opciones = df.select(pl.col(columna).unique()).to_series().sort().to_list()
    seleccion = st.selectbox(label, opciones, format_func=str.capitalize, key=key)
    return df.filter(pl.col(columna) == seleccion)


def create_bar_chart(df: pl.DataFrame, titulo: str, idx: int):
    fig = px.bar(
        df.filter(pl.col("conceptos") == titulo),
        x="valor",
        y="seccion",
        title=f"{idx + 1}. {titulo}",
    )
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        xaxis_title="Progreso",
        yaxis_title="",
        xaxis_range=[0, 3],
        margin=dict(l=15, r=10, t=50, b=10),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(15,15,15,0.3)", dtick=1, griddash="dash"
        ),
        yaxis=dict(
            showgrid=False,
            gridcolor="rgba(128,128,128,0.3)",
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="rgba(15,15,15,0.3)", width=1),
                fillcolor="rgba(0,0,0,0)",
                layer="above",
            )
        ],
    )
    st.plotly_chart(fig, use_container_width=True)
