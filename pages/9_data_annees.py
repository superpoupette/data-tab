import streamlit as st

from scripts.data_loader import load_year

from scripts.importation_2025 import prepare_2025


data2025 = prepare_2025(
    "data/2025.csv"
)


data2024 = load_year(2024)


st.title("📚 Données 2025")

st.dataframe(
    data2025,
    use_container_width=True
)


st.title("📚 Données 2024")

st.dataframe(
    data2024,
    use_container_width=True
)