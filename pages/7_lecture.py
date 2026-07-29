import streamlit as st
import pandas as pd

from scripts.data_loader import load_babelio


st.title("📚 Lecture")


# =====================
# Chargement données
# =====================

livres = load_babelio()
st.write(livres.columns.tolist())
st.write(livres.head())

# =====================
# Livres lus
# =====================

livres_lus = livres[
    livres["Statut"] == "Lu"
].copy()



# =====================
# KPI
# =====================

col1, col2 = st.columns(2)


with col1:

    st.metric(
        "Livres lus",
        len(livres_lus)
    )


with col2:

    note_moyenne = (
        livres_lus["Note"]
        .astype(float)
        .mean()
    )

    st.metric(
        "Note moyenne",
        f"{note_moyenne:.1f}/5"
    )



# =====================
# Livres lus par mois
# =====================

st.subheader("📅 Livres lus par mois")


livres_lus["date_entree"] = pd.to_datetime(
    livres_lus["Date d`entrée dans Babelio"],
    errors="coerce"
)


livres_lus["mois"] = (
    livres_lus["date_entree"]
    .dt.to_period("M")
    .astype(str)
)


livres_par_mois = (
    livres_lus
    .groupby("mois")
    .size()
)


st.bar_chart(
    livres_par_mois
)