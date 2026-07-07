import streamlit as st

from scripts.importation_2025 import prepare_2025


data2025, danse = prepare_2025(
    "data/2025.csv"
)

st.title("💃 Dashboard Danse")


# Temps total par titre
temps_par_titre = (
    danse
    .groupby("titre", as_index=False)["duree_min"]
    .sum()
    .sort_values(
        "duree_min",
        ascending=False
    )
)

temps_par_titre = temps_par_titre.rename(
    columns={
        "duree_min": "temps_total_min"
    }
)


st.subheader("🎵 Temps total par musique")

st.dataframe(
    temps_par_titre,
    use_container_width=True
)