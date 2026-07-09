import streamlit as st
from datetime import date

from scripts.data_entry.dataframe import create_today_dataframe

st.title("Today")

st.write(f"📅 Aujourd'hui : {date.today().strftime('%d/%m/%Y')}")

best_moment = st.text_area(
    "Best moment",
    placeholder="Quel a été le meilleur moment de ta journée ?"
)

df = create_today_dataframe()

st.subheader("Tableau des données")

st.dataframe(df, use_container_width=True)