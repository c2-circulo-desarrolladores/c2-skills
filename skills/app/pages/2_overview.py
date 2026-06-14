
import polars as pl
import streamlit as st

from skills.app.shared import create_bar_chart
from skills.io import encuesta_parser

fundamentals = encuesta_parser.main()

st.set_page_config(
    page_title="Círculo de Desarrolladores Open Source (C2) - Skills Dashboard",
    layout="wide",
)

st.title("Conocimiento del equipo")

# Selector de miembro
col1, col2 = st.columns(2)
with col2:
    st.markdown("#")
with col1:
    tema_escogido = st.selectbox(
        "Selecciona un tema",
        fundamentals["tema"].unique(maintain_order=True).to_list(),
    )
    tema_df = fundamentals.filter(pl.col("tema") == tema_escogido)
    tema_grouped = tema_df.group_by(["conceptos", "seccion"]).agg(pl.col("valor").mean())
    conceptos = tema_grouped["conceptos"].unique(maintain_order=True).to_list()
    for idx, concepto in enumerate(conceptos):
        if idx % 2:
            with col2:
                create_bar_chart(tema_grouped, concepto, idx)
        else:
            create_bar_chart(tema_grouped, concepto, idx)

  