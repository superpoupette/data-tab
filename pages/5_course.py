import streamlit as st

from scripts.importation_strava import charger_donnees_strava


st.set_page_config(
    page_title="Course",
    page_icon="🏃",
    layout="wide"
)



st.title("🏃 Dashboard Course")



df = charger_donnees_strava()

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)