import plotly.graph_objects as go
import streamlit as st
from conf import MIEMBROS
from models import MemberSkills, SkillSection
from parse_skills import parse_skills_all


def calculate_progress(sections: list[SkillSection]) -> dict:
    """Calcula progreso total de una lista de secciones"""
    total = sum(len(section.skills) for section in sections)
    completed = sum(
        sum(1 for skill in section.skills if skill.checked) for section in sections
    )
    percentage = round((completed / total * 100) if total > 0 else 0)
    return {"completed": completed, "total": total, "percentage": percentage}


def create_spider_chart(sections: list[SkillSection]) -> go.Figure:
    """Crea un gráfico spider para los perfiles especializados"""
    categories = []
    percentages = []

    for section in sections:
        total = len(section.skills)
        completed = sum(1 for skill in section.skills if skill.checked)
        percentage = (completed / total * 100) if total > 0 else 0

        categories.append(section.title)
        percentages.append(percentage)

    # Cerrar el polígono agregando el primer punto al final
    categories_closed = categories + [categories[0]]
    percentages_closed = percentages + [percentages[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=percentages_closed,
            theta=categories_closed,
            fill="toself",
            name="Progreso",
            line=dict(color="#1f77b4", width=2),
            fillcolor="rgba(31, 119, 180, 0.3)",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix="%",
                gridcolor="rgba(128, 128, 128, 0.2)",
            ),
            angularaxis=dict(gridcolor="rgba(128, 128, 128, 0.2)"),
        ),
        showlegend=False,
        height=500,
        margin=dict(l=80, r=80, t=40, b=40),
    )

    return fig


def render_dashboard(members: list[MemberSkills]):
    """Renderiza el dashboard con Streamlit"""
    st.set_page_config(
        page_title="Círculo de Desarrolladores Open Source (C2) - Skills Dashboard", layout="wide"
    )

    st.title("🐍 Círculo de Desarrolladores Open Source (C2) - Skills Dashboard")

    # Selector de miembro
    member_names = [m.name for m in members]
    selected_member = st.selectbox("Selecciona un miembro:", member_names)

    member = next(m for m in members if m.name == selected_member)

    # Progress general
    st.header(f"📊 Progreso de {member.name}")

    col1, col2 = st.columns(2)

    with col1:
        if member.fundamentals:
            st.subheader("Fundamentals")
            fund_progress = calculate_progress(member.fundamentals)
            st.progress(fund_progress["percentage"] / 100)
            st.metric(
                "Completado",
                f"{fund_progress['completed']}/{fund_progress['total']}",
                f"{fund_progress['percentage']}%",
            )

    with col2:
        if member.profiles:
            st.subheader("Perfiles Especializados")
            prof_progress = calculate_progress(member.profiles)
            st.progress(prof_progress["percentage"] / 100)
            st.metric(
                "Completado",
                f"{prof_progress['completed']}/{prof_progress['total']}",
                f"{prof_progress['percentage']}%",
            )

    # Spider Chart para Perfiles
    if member.profiles:
        st.header("🕸️ Visualización de Perfiles")
        spider_fig = create_spider_chart(member.profiles)
        st.plotly_chart(spider_fig, use_container_width=True)

    # Detalles por sección
    st.header("📝 Detalle de Skills")

    # Fundamentals
    if member.fundamentals:
        st.subheader("🔧 Python Fundamentals")
        for section in member.fundamentals:
            with st.expander(
                f"{section.title} ({sum(1 for s in section.skills if s.checked)}/{len(section.skills)})"
            ):
                for skill in section.skills:
                    st.checkbox(
                        skill.name,
                        value=skill.checked,
                        key=f"fund_{section.title}_{skill.name}",
                        disabled=True,
                    )

    # Profiles
    if member.profiles:
        st.subheader("🎯 Perfiles Especializados - Detalle")
        for section in member.profiles:
            with st.expander(
                f"{section.title} ({sum(1 for s in section.skills if s.checked)}/{len(section.skills)})"
            ):
                for skill in section.skills:
                    st.checkbox(
                        skill.name,
                        value=skill.checked,
                        key=f"prof_{section.title}_{skill.name}",
                        disabled=True,
                    )


def main():
    members = parse_skills_all(MIEMBROS)
    render_dashboard(members)


if __name__ == "__main__":
    main()
