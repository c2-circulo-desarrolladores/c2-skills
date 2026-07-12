import plotly.express as px
import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS


def render_header() -> None:
    st.title("🎯 Ranking del equipo")
    st.text(
        "Visualiza el rendimiento de cada integrante e identifica oportunidades de mejora."
    )


def render_filtros() -> pl.DataFrame:
    col1, col2 = st.columns(2)
    with col1:
        encuesta_sel = st.selectbox(
            "Filtrar por encuesta:",
            ["Todas"] + FUNDAMENTALS["encuesta"].unique(maintain_order=True).to_list(),
        )
    with col2:
        tema_options = (
            FUNDAMENTALS["tema"].unique(maintain_order=True).to_list()
            if encuesta_sel == "Todas"
            else FUNDAMENTALS.filter(pl.col("encuesta") == encuesta_sel)["tema"]
            .unique(maintain_order=True)
            .to_list()
        )
        tema_sel = st.selectbox("Filtrar por tema:", ["Todas"] + tema_options)

    df = FUNDAMENTALS
    if encuesta_sel != "Todas":
        df = df.filter(pl.col("encuesta") == encuesta_sel)
    if tema_sel != "Todas":
        df = df.filter(pl.col("tema") == tema_sel)

    concepto_options = df["conceptos"].unique(maintain_order=True).to_list()
    concepto_sel = st.multiselect("Filtrar por conceptos:", concepto_options)
    if concepto_sel:
        df = df.filter(pl.col("conceptos").is_in(concepto_sel))

    return df


def render_ranking(df: pl.DataFrame) -> None:
    st.subheader("Ranking del equipo")
    necesidad_df = (
        df.group_by("miembro", maintain_order=True)
        .agg((pl.col("valor").mean() / 3 * 100).round(1).alias("nivel"))
        .sort("nivel", descending=True)
    )
    fig_necesidad = px.bar(
        necesidad_df,
        x="miembro",
        y="nivel",
        color="nivel",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig_necesidad, width="stretch")


def render_heatmap(df: pl.DataFrame) -> None:
    st.subheader("🗺️ Mapa de calor: miembro x encuesta")
    heatmap_df = df.group_by(["miembro", "encuesta"], maintain_order=True).agg(
        (pl.col("valor").mean() / 3 * 100).round(1).alias("nivel")
    )
    pivot_df = heatmap_df.pivot(
        values="nivel",
        index="miembro",
        on="encuesta",
        aggregate_function="first",
    )

    miembros = pivot_df["miembro"].to_list()
    encuestas = [c for c in pivot_df.columns if c != "miembro"]
    matriz = pivot_df.drop("miembro").to_numpy()

    fig_heatmap = px.imshow(
        matriz,
        x=encuestas,
        y=miembros,
        color_continuous_scale="RdYlGn",
        aspect="auto",
        text_auto=True,
        labels=dict(color="Nivel (%)"),
    )
    fig_heatmap.update_xaxes(side="top")
    st.plotly_chart(fig_heatmap, width="stretch")


def main() -> None:
    render_header()
    df = render_filtros()

    st.divider()
    render_ranking(df)

    st.divider()
    render_heatmap(df)
    st.divider()


main()
