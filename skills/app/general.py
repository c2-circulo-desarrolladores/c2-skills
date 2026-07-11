import streamlit as st

from skills.app.shared import FUNDAMENTALS
from skills.app.shared.dashboard import (
    agrupar_por_tema,
    calcular_progreso,
    render_bar_charts,
)
from skills.app.shared.figures import create_card
from skills.app.shared.utils import seleccionar_y_filtrar

st.set_page_config(
    page_title="C2 - Skills Dashboard",
    layout="wide",
)
st.title("🐍 C2 - Skills Dashboard")

st.title("Conocimiento del equipo")
st.text("Evalúa el nivel de conocimiento general del equipo")

col1, col2 = st.columns(2)

# Crear tarjetas
with col2:
    create_card(texto="Progreso", metric=calcular_progreso(FUNDAMENTALS, "encuesta"))
    st.markdown("#")
with col1:
    create_card(texto="Miembros evaluados", metric=FUNDAMENTALS.n_unique("miembro"))

    # Filtro de encuesta
    tema_df = seleccionar_y_filtrar(
        FUNDAMENTALS, columna="encuesta", label="Selecciona una encuesta", key="encuesta"
    )

# Bar charts por tema
tema_grouped = agrupar_por_tema(tema_df)
render_bar_charts(tema_grouped, col1, col2)