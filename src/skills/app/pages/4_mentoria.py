import plotly.express as px
import polars as pl
import streamlit as st

from skills.app.shared import FUNDAMENTALS


def render_header() -> None:
    st.title("Plan de Mentoría")
    st.text("Identifica oportunidades de mejora.")


def render_gap_analysis(df: pl.DataFrame) -> None:
    st.subheader("🔻 Temas más débiles del equipo")
    gap_df = (
        df.group_by("tema", maintain_order=True)
        .agg((pl.col("valor").mean() / 3 * 100).round(1).alias("nivel"))
        .sort("nivel")
        .head(15)
        .reverse()
    )
    fig_gap = px.bar(
        gap_df,
        x="nivel",
        y="tema",
        orientation="h",
        color="nivel",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig_gap, width="stretch")


def main():
    render_header()
    render_gap_analysis(FUNDAMENTALS)


main()
