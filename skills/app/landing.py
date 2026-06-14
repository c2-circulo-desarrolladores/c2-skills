
import polars as pl
import streamlit as st

from skills.app.shared import create_bar_chart, seleccionar_y_filtrar
from skills.io import encuesta_parser

fundamentals = encuesta_parser.main()

st.set_page_config(
    page_title="Círculo de Desarrolladores Open Source (C2) - Skills Dashboard",
    layout="wide",
)

st.title("🐍 Círculo de Desarrolladores Open Source (C2) - Skills Dashboard")

# Selector de miembro
col1, col2 = st.columns(2)
with col2:
    st.markdown("#")
    st.markdown("#")
with col1:
    member_names = [miembro for miembro in fundamentals["miembro"].unique().sort()]
    selected_member = st.selectbox(
        "Selecciona un miembro:", member_names, format_func=str.capitalize
    )
    # st.header(f"📊 Progreso de {selected_member}")

    # Filtrar datos de miembro seleccionado
    member_df = fundamentals.filter(pl.col("miembro") == selected_member)
    # Progress general

    tema_df = seleccionar_y_filtrar(
        member_df, "tema", "Selecciona un tema:", f"tema_{selected_member}"
    )

    concepto_df = tema_df.group_by(
        ["conceptos", "seccion", "valor"], maintain_order=True
    ).agg()
    conceptos = tema_df["conceptos"].unique(maintain_order=True).to_list()
    for idx, concepto in enumerate(conceptos):
        if idx % 2:
            with col2:
                create_bar_chart(concepto_df, concepto, idx)
        else:
            create_bar_chart(concepto_df, concepto, idx)

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
