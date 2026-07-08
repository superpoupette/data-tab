import streamlit as st


from scripts.importation_tvtime import tab_tv

tvtime = tab_tv()

st.title("Données TV Time")

st.dataframe(
    tvtime,
    use_container_width=True
)