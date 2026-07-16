import streamlit as st

from scripts.importation_strava import charger_donnees_strava



st.set_page_config(
    page_title="Course",
    page_icon="🏃",
    layout="wide"
)

st.write(df.columns[:5])
st.write(df["Nom de l'activité"].head())

st.title("🏃 Dashboard Course")

df = charger_donnees_strava()

st.subheader("Données Strava")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)