import streamlit as st

from scripts.importation_2025 import prepare_2025
from scripts.importation_2024 import prepare_2024

data2025 = prepare_2025(
    "data/2025.csv"
)

data2024 = prepare_2024(
    "data/2024.csv"
)

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

