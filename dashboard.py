#py -3.12 -m streamlit run dashboard.py

import streamlit as st

from gestion_sport import charger_tableau_sport

st.title("📊 Mon tableau de bord personnel")

st.write("Suivi des activités sportives")

df_sport = charger_tableau_sport()

st.dataframe(
    df_sport,
    use_container_width=True,
    hide_index=True,
)