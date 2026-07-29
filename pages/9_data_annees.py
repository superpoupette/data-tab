import streamlit as st

from scripts.data_loader import load_year


data2024 = load_year(2024)

data2025 = load_year(2025)


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