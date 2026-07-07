import streamlit as st
import pandas as pd

from scripts.importation_babelio import prepare_babelio


st.title("📚 Lecture")


livres = prepare_babelio(
    "data/biblio.csv"
)


livres_lus = livres[
    livres["Statut"] == "Lu"
]


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Livres lus",
        len(livres_lus)
    )

with col2:
    st.metric(
        "Note moyenne",
        f"{livres_lus['Note'].mean():.1f}/5"
    )


st.subheader("📅 Livres lus par mois")


livres_lus["date_entree"] = (
    livres_lus["Date d`entrée dans Babelio"]
    .pipe(lambda x: pd.to_datetime(x))
)

livres_lus["mois"] = (
    livres_lus["date_entree"]
    .dt.to_period("M")
)


st.bar_chart(
    livres_lus.groupby("mois").size()
)