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
        "Temps d'apprentissage global",
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
        "Nombre de chorégraphies apprises",
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
        infos = [
            derniere_choree["titre"],
            derniere_choree["artiste"],
            derniere_choree["choregraphe"]
        ]

        infos = [
            str(info).strip()
            for info in infos
            if pd.notna(info) and str(info).strip()
        ]

        titre_derniere_choree = " - ".join(infos)

        st.metric(
            "Dernière chorégraphie apprise",
            titre_derniere_choree
        )
    else:
        st.metric(
            "Dernière chorégraphie apprise",
            "Aucune"
        )


st.divider()
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

    # Titre et liste déroulante sur la même ligne
    col_titre, col_tri = st.columns([2, 1])

    with col_titre:
        st.subheader("Top chorégraphies")

    with col_tri:
        classement = st.selectbox(
            "Classement",
            ["Plus de temps", "Moins de temps"],
            key="classement_chorees",
            label_visibility="collapsed"
        )

    # Garder les chorégraphies avec un temps positif
    chorees = danse_recap[
        danse_recap["duree_apprentissage"] > 0
    ].copy()

    # Classement global : du plus long au plus court
    chorees = chorees.sort_values(
        "duree_apprentissage",
        ascending=False
    ).reset_index(drop=True)

    # Garder les rangs du classement global
    chorees["place"] = chorees.index + 1

    if classement == "Plus de temps":
        affichage = chorees.head(10)
    else:
        # Les 10 chorégraphies les plus rapides,
        # affichées de la plus longue à la plus courte
        affichage = chorees.tail(10)

    if affichage.empty:
        st.info(
            "Aucune chorégraphie avec un temps "
            "d'apprentissage renseigné."
        )
    else:
        for _, choree in affichage.iterrows():

            artiste = (
                str(choree["artiste"]).strip()
                if pd.notna(choree["artiste"])
                else ""
            )

            titre = (
                str(choree["titre"]).strip()
                if pd.notna(choree["titre"])
                else ""
            )

            choregraphe = (
                str(choree["choregraphe"]).strip()
                if pd.notna(choree["choregraphe"])
                else ""
            )

            # Construire le nom
            nom = f"{artiste} - {titre}" if artiste else titre

            if choregraphe:
                nom += f" ({choregraphe})"

            # Durée en heures et minutes
            temps = int(choree["duree_apprentissage"])
            heures = temps // 60
            minutes = temps % 60

            if heures > 0 and minutes > 0:
                temps_formate = f"{heures}h{minutes:02d}"
            elif heures > 0:
                temps_formate = f"{heures}h"
            else:
                temps_formate = f"{minutes}min"

            st.write(
                f"{choree['place']}. {nom} : {temps_formate}"
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
