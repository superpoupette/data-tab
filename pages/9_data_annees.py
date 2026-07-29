import streamlit as st

from scripts.importation_2025 import prepare_2025
from scripts.importation_2024 import prepare_2024
from scripts.google_drive import load_csv_from_drive
from scripts.importation_2024 import clean_csv

data2025 = prepare_2025(
    "data/2025.csv"
)


data2024 = load_csv_from_drive(
    "17onD34HL2QKC4OP0oPrvt_ynfq63XO0Z"
)

data2024 = clean_csv(
    data2024
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

