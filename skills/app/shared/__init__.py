import streamlit as st

from skills.io import encuesta_parser


@st.cache_data
def load_fundamentals():
    return encuesta_parser.main()

FUNDAMENTALS = load_fundamentals()
