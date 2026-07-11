import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS
from skills.app.shared.figures import create_card
from skills.app.shared.utils import (
    agrupar_por_tema,
    calcular_progreso,
    render_bar_charts,
    seleccionar_y_filtrar,
)

st.set_page_config(
    page_title="Círculo de Desarrolladores Open Source (C2) - Skills Dashboard",
    layout="wide",
)
st.title("🐍 Círculo de Desarrolladores Open Source (C2) - Skills Dashboard")

# Filtros
col1, col2 = st.columns(2)
with col1:
    # Filtro de miembro
    member_names = [miembro for miembro in FUNDAMENTALS["miembro"].unique().sort()]
    selected_member = st.selectbox(
        "Selecciona un miembro:", member_names, format_func=str.capitalize
    )
    member_df = FUNDAMENTALS.filter(pl.col("miembro") == selected_member)

    # Filtro de encuesta
    tema_df = seleccionar_y_filtrar(
        member_df,
        columna="encuesta",
        label="Selecciona una encuesta:",
        key=f"encuesta_{selected_member}",
    )

# Tarjeta de progreso
with col2:
    create_card(texto="Progreso", metric=calcular_progreso(member_df, "conceptos"))

# Bar charts por tema
tema_grouped = agrupar_por_tema(tema_df)
render_bar_charts(tema_grouped, col1, col2)