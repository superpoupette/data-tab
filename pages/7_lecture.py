import streamlit as st

from scripts.data_loader import load_babelio


st.set_page_config(
    page_title="Lecture",
    page_icon="📖",
    layout="wide"
)


st.title("📖 Lecture")


# =====================
# Chargement données
# =====================

livres = load_babelio()


# =====================
# Récapitulatif
# =====================

st.subheader("Récapitulatif")

st.dataframe(
    livres,
    use_container_width=True
)