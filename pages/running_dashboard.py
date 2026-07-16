import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Running", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/strava_activities.csv", encoding="latin1")
    cols = {c:c.encode("latin1","ignore").decode("utf-8","ignore") for c in df.columns}
    df.rename(columns=cols,inplace=True)
    date_col=[c for c in df.columns if "Date de l" in c][0]
    df["Date"]=pd.to_datetime(df[date_col], errors="coerce")
    def pick(name):
        for c in df.columns:
            if name.lower() in c.lower():
                return c
        return None
    mapping={
        "Distance":pick("Distance"),
        "Durée":pick("Durée de déplacement"),
        "Calories":pick("Calories"),
        "D+":pick("Dénivelé positif"),
        "FC moy":pick("Fréquence cardiaque moyenne"),
        "Type":pick("Type d'activité"),
        "Nom":pick("Nom de l'activité")
    }
    out=pd.DataFrame()
    out["Date"]=df["Date"]
    for k,v in mapping.items():
        out[k]=df[v] if v else None
    out["Distance"]=pd.to_numeric(out["Distance"],errors="coerce")
    out["Calories"]=pd.to_numeric(out["Calories"],errors="coerce")
    out["D+"]=pd.to_numeric(out["D+"],errors="coerce")
    out["FC moy"]=pd.to_numeric(out["FC moy"],errors="coerce")
    out["Année"]=out["Date"].dt.year
    return out

df=load_data()
st.title("🏃 Dashboard Running")

year=st.sidebar.selectbox("Année",["Toutes"]+sorted(df["Année"].dropna().unique().tolist()))
if year!="Toutes":
    df=df[df["Année"]==year]

c1,c2,c3,c4=st.columns(4)
c1.metric("Distance totale (km)",f"{df['Distance'].sum():.1f}")
c2.metric("Sorties",len(df))
c3.metric("D+ total (m)",f"{df['D+'].sum():.0f}")
c4.metric("Calories",f"{df['Calories'].sum():.0f}")

tab1,tab2,tab3=st.tabs(["Vue générale","Performances","Historique"])

with tab1:
    monthly=df.groupby(df["Date"].dt.to_period("M"))["Distance"].sum().reset_index()
    monthly["Date"]=monthly["Date"].astype(str)
    st.plotly_chart(px.bar(monthly,x="Date",y="Distance",title="Kilomètres par mois"),use_container_width=True)

with tab2:
    st.plotly_chart(px.scatter(df,x="Distance",y="FC moy",hover_name="Nom",title="Distance vs FC"),use_container_width=True)
    st.plotly_chart(px.scatter(df,x="Distance",y="D+",hover_name="Nom",title="Distance vs D+"),use_container_width=True)

with tab3:
    st.dataframe(df.sort_values("Date",ascending=False),use_container_width=True)
