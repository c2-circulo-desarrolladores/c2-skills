import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS
from skills.app.shared.figures import create_bar_chart, create_card
from skills.app.shared.utils import seleccionar_y_filtrar

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
    progreso = progreso = (
        str(
            round(
                member_df.group_by(["conceptos"], maintain_order=True)
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
    create_card(texto="Progreso", metric=progreso)

#
with col1:
    tema_grouped = tema_df.group_by(["tema", "seccion"], maintain_order=True).agg(
        pl.col("valor").mean()
    )
    temas = tema_grouped["tema"].unique(maintain_order=True).to_list()

    # Crear un bar chart por cada tema
    for idx, tema in enumerate(temas):
        if idx % 2:
            with col2:
                tema_filtrado = tema_grouped.filter(pl.col("tema") == tema)
                create_bar_chart(tema_filtrado, tema, idx)
        else:
            tema_filtrado = tema_grouped.filter(pl.col("tema") == tema)
            create_bar_chart(tema_filtrado, tema, idx)

    #
#     fund_progress = calculate_progress(member.fundamentals)
#     st.progress(fund_progress["percentage"] / 100)
#     st.metric(
#         "Completado",
#         f"{fund_progress['completed']}/{fund_progress['total']}",
#         f"{fund_progress['percentage']}%",
#     )

# with col2:
#     if member.profiles:
#         st.subheader("Perfiles Especializados")
#         prof_progress = calculate_progress(member.profiles)
#         st.progress(prof_progress["percentage"] / 100)
#         st.metric(
#             "Completado",
#             f"{prof_progress['completed']}/{prof_progress['total']}",
#             f"{prof_progress['percentage']}%",
#         )

# # Spider Chart para Perfiles
# if member.profiles:
#     st.header("🕸️ Visualización de Perfiles")
#     spider_fig = create_spider_chart(member.profiles)
#     st.plotly_chart(spider_fig, use_container_width=True)

# # Detalles por sección
# st.header("📝 Detalle de Skills")

# # Fundamentals
# if member.fundamentals:
#     st.subheader("🔧 Python Fundamentals")
#     for section in member.fundamentals:
#         with st.expander(
#             f"{section.title} ({sum(1 for s in section.skills if s.checked)}/{len(section.skills)})"
#         ):
#             for skill in section.skills:
#                 st.checkbox(
#                     skill.name,
#                     value=skill.checked,
#                     key=f"fund_{section.title}_{skill.name}",
#                     disabled=True,
#                 )

# # Profiles
# if member.profiles:
#     st.subheader("🎯 Perfiles Especializados - Detalle")
#     for section in member.profiles:
#         with st.expander(
#             f"{section.title} ({sum(1 for s in section.skills if s.checked)}/{len(section.skills)})"
#         ):
#             for skill in section.skills:
#                 st.checkbox(
#                     skill.name,
#                     value=skill.checked,
#                     key=f"prof_{section.title}_{skill.name}",
#                     disabled=True,
#                 )
