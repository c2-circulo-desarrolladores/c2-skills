import plotly.express as px
import polars as pl
import streamlit as st

from .colors import C2Colors


def create_card(texto: str, metric: str | int | float):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #ac001d 0%, #5a0010 100%);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            color: white;
            margin-bottom: 1rem;
        ">
            <div style="font-size: 14px; opacity: 0.9; letter-spacing: 1px;">{texto}</div>
            <div style="font-size: 48px; font-weight: bold;">{metric}</div>
        </div>
    """,
        unsafe_allow_html=True,
    )


# TODO: Separate this logic
def create_bar_chart(df: pl.DataFrame, titulo: str, idx: int):
    fig = px.bar(
        df.filter(pl.col("conceptos") == titulo),
        x="valor",
        y="seccion",
        title=f"{idx + 1}. {titulo}",
    )
    fig.update_layout(
        title_font_size=20,
        title_x=0.5,
        xaxis_title="Progreso",
        yaxis_title="",
        xaxis_range=[0, 3],
        margin=dict(l=15, r=10, t=50, b=10),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.5)",
            dtick=1,
            griddash="dash",
        ),
        yaxis=dict(
            showgrid=False,
            gridcolor="rgba(128,128,128,0.3)",
        ),
        shapes=[
            dict(
                type="rect",
                xref="paper",
                yref="paper",
                x0=0,
                y0=0,
                x1=1,
                y1=1,
                line=dict(color="rgba(255, 255, 255, 0.5)", width=1),
                fillcolor="rgba(0,0,0,0)",
                layer="above",
            )
        ],
    )
    fig.update_traces(marker_color=C2Colors.RED)
    st.plotly_chart(fig)
