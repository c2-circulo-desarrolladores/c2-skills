import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS
from skills.app.shared.figures import create_bar_chart, create_card
from skills.app.shared.utils import seleccionar_y_filtrar

st.set_page_config(
    page_title="C2 - Skills Dashboard",
    layout="wide",
)
st.title("🐍 C2 - Skills Dashboard")

st.title("Conocimiento del equipo")
st.text("Evalúa el nivel de conocimiento general del equipo")
progreso = (
    str(
        round(
            FUNDAMENTALS.group_by(["encuesta"], maintain_order=True)
            .agg(pl.col("valor").mean())
            .mean()
            .select(pl.col("valor"))
            .item()
            / 3
            * 100,
            ndigits=2,
        )
    )
    + "%"
)
col1, col2 = st.columns(2)

# Crear tarjetas
with col2:
    create_card(texto="Progreso", metric=progreso)
    st.markdown("#")
with col1:
    create_card(texto="Miembros evaluados", metric=FUNDAMENTALS.n_unique("miembro"))

    # Filtro de encuesta
    tema_df = seleccionar_y_filtrar(
        FUNDAMENTALS, columna="encuesta", label="Selecciona una encuesta", key="encuesta"
    )

    # Agrupar por tema y seccion, y agregar la media de los puntajes
    tema_grouped = tema_df.group_by(["tema", "seccion"], maintain_order=True).agg(
        pl.col("valor").mean()
    )
    conceptos = tema_grouped["tema"].unique(maintain_order=True).to_list()

    # Crear un bar chart por cada concepto
    for idx, tema in enumerate(conceptos):
        if idx % 2:
            with col2:
                tema_filtrado = tema_grouped.filter(pl.col("tema") == tema)
                create_bar_chart(tema_filtrado.reverse(), tema, idx)
        else:
            tema_filtrado = tema_grouped.filter(pl.col("tema") == tema)
            create_bar_chart(tema_filtrado.reverse(), tema, idx)
