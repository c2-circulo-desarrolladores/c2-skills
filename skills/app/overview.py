import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS, create_bar_chart, create_card

st.set_page_config(
    page_title="C2 - Skills Dashboard",
    layout="wide",
)

st.title("🐍 C2 - Skills Dashboard")

st.title("Conocimiento del equipo")
st.text("Evalúa el nivel de conocimiento general del equipo")
progreso = str(
    round(
        FUNDAMENTALS.group_by(["conceptos"], maintain_order=True)
        .agg(pl.col("valor").mean())
        .mean()
        .select(pl.col("valor"))
        .item()
        / 3
        * 100,
        ndigits=2,
    )
) + "%"
col1, col2 = st.columns(2)
with col2:
    create_card(texto="Progreso", metric=progreso)
    st.markdown("#")
with col1:
    create_card(texto="Miembros evaluados", metric=FUNDAMENTALS.n_unique("miembro"))
    tema_escogido = st.selectbox(
        "Selecciona un tema",
        FUNDAMENTALS["tema"].unique(maintain_order=True).to_list(),
    )
    tema_df = FUNDAMENTALS.filter(pl.col("tema") == tema_escogido)
    tema_grouped = tema_df.group_by(["conceptos", "seccion"], maintain_order=True).agg(
        pl.col("valor").mean()
    )
    conceptos = tema_grouped["conceptos"].unique(maintain_order=True).to_list()
    for idx, concepto in enumerate(conceptos):
        if idx % 2:
            with col2:
                create_bar_chart(tema_grouped.reverse(), concepto, idx)
        else:
            create_bar_chart(tema_grouped.reverse(), concepto, idx)
