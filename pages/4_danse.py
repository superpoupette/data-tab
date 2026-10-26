import streamlit as st
import pandas as pd
import plotly.express as px

from scripts.danse.google_sheet import load_danse_google_sheet


# =========================
# Chargement Google Sheet
# =========================

danse_recap = load_danse_google_sheet()


danse_recap["date_debut"] = pd.to_datetime(
    danse_recap["date_debut"],
    errors="coerce"
)

for col in ["date_fin", "date_fin_2", "date_fin_3"]:
    if col not in danse_recap.columns:
        danse_recap[col] = pd.NaT

    danse_recap[col] = pd.to_datetime(
        danse_recap[col],
        errors="coerce"
    )


# Valeurs numériques

for col in [
    "duree_apprentissage",
    "nombre_seance",
    "duree_seance"
]:
    danse_recap[col] = pd.to_numeric(
        danse_recap[col],
        errors="coerce"
    ).fillna(0)



st.title("💃 Dashboard Danse")

```python
# =========================
# Indicateurs principaux
# =========================

col1, col2, col3 = st.columns(3)

# -------------------------
# Temps d'apprentissage global
# -------------------------

with col1:
    temps_total_min = danse_recap["duree_apprentissage"].sum()

    heures = int(temps_total_min // 60)
    minutes = int(temps_total_min % 60)

    st.metric(
        "⏱️ Temps d'apprentissage global",
        f"{heures}h{minutes:02d}"
    )

# -------------------------
# Nombre de chorégraphies apprises
# -------------------------

with col2:
    nb_chorees = (
        danse_recap["statut"]
        .fillna("")
        .str.lower()
        .str.strip()
        .eq("termine")
        .sum()
    )

    st.metric(
        "💃 Chorégraphies apprises",
        int(nb_chorees)
    )

# -------------------------
# Dernière chorégraphie apprise
# -------------------------

with col3:
    dates_fin = danse_recap[
        ["date_fin", "date_fin_2", "date_fin_3"]
    ].max(axis=1)

    derniere_choree = danse_recap.loc[
        dates_fin.idxmax()
    ] if dates_fin.notna().any() else None

    if derniere_choree is not None:
        titre_derniere_choree = derniere_choree["titre"]

        st.metric(
            "🆕 Dernière chorégraphie apprise",
            titre_derniere_choree
        )
    else:
        st.metric(
            "🆕 Dernière chorégraphie apprise",
            "Aucune"
        )
```



# =========================
# Graphiques principaux
# =========================


col1, col2 = st.columns(2)



# -------------------------
# Styles
# -------------------------

with col1:

    st.subheader(
        "Répartition des styles"
    )


    styles = (
        danse_recap
        .groupby("style")
        .size()
        .reset_index(
            name="nombre"
        )
        .sort_values(
            "nombre",
            ascending=False
        )
    )


    fig_style = px.pie(
        styles,
        values="nombre",
        names="style",
        hole=0.3
    )


    st.plotly_chart(
        fig_style,
        use_container_width=True
    )



# -------------------------
# Artistes
# -------------------------

with col2:

    st.subheader(
        "Top 10 artistes"
    )


    artistes = (
        danse_recap[
            danse_recap["duree_apprentissage"] > 0
        ]
        .groupby("artiste")
        .size()
        .reset_index(
            name="nombre_chorees"
        )
        .sort_values(
            "nombre_chorees",
            ascending=False
        )
        .head(10)
    )


    fig_artistes = px.bar(
        artistes,
        x="nombre_chorees",
        y="artiste",
        orientation="h",
        labels={
            "nombre_chorees":
                "Nombre de chorégraphies",
            "artiste":
                "Artiste"
        }
    )


    st.plotly_chart(
        fig_artistes,
        use_container_width=True
    )




# =========================
# Evolution des chorégraphies terminées
# =========================

st.subheader(
    "Chorégraphies terminées par mois"
)

# Rassembler toutes les dates des trois colonnes
dates_fin = pd.concat(
    [
        danse_recap["date_fin"],
        danse_recap["date_fin_2"],
        danse_recap["date_fin_3"]
    ],
    ignore_index=True
)

# Compter les dates de fin par mois
evolution = (
    dates_fin
    .dropna()
    .dt.to_period("M")
    .astype(str)
    .value_counts()
    .sort_index()
    .rename_axis("mois")
    .reset_index(name="nombre")
)

fig_mois = px.line(
    evolution,
    x="mois",
    y="nombre",
    markers=True,
    labels={
        "mois": "Mois",
        "nombre": "Chorégraphies terminées"
    }
)

st.plotly_chart(
    fig_mois,
    use_container_width=True
)



# =========================
# Top chorégraphies
# =========================

st.subheader(
    "Top 10 chorégraphies par temps d'apprentissage"
)


top_chorees = (
    danse_recap
    .sort_values(
        "duree_apprentissage",
        ascending=False
    )
    .head(10)
)


fig_top = px.bar(
    top_chorees,
    y="titre",
    x="duree_apprentissage",
    orientation="h",
    labels={
        "titre":
            "Chorégraphie",
        "duree_apprentissage":
            "Temps (min)"
    }
)


st.plotly_chart(
    fig_top,
    use_container_width=True
)
