import streamlit as st

from scripts.importation_2025 import prepare_2025

data2025 = prepare_2025(
    "data/2025.csv"
)

st.title("📚 Données 2025")

st.dataframe(
    data2025,
    use_container_width=True
)