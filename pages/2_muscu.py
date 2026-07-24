import streamlit as st
import altair as alt
from scripts.importation_hevy import prepare_data


st.title("🏋️ Entraînement")


workouts, sessions = prepare_data(
    "data/workouts.csv",
    "data/exercices.csv"
)


# Indicateurs principaux

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Nombre de séances",
        len(sessions)
    )

with col2:
    st.metric(
        "Volume total",
        f"{sessions['volume_total'].sum():,.0f} kg"
    )

with col3:
    st.metric(
        "Durée totale",
        f"{sessions['duree_minutes'].sum()/60:.1f} h"
    )

with col4:
    st.metric(
        "Durée moyenne séance",
        f"{sessions['duree_minutes'].mean():.0f} min"
    )




st.subheader("Temps total d'entraînement par mois")

# Recréation propre du mois
sessions["mois"] = sessions["start_time"].dt.to_period("M").astype(str)

temps_par_mois = (
    sessions
    .groupby("mois", as_index=False)["duree_minutes"]
    .sum()
)

temps_par_mois["heures"] = temps_par_mois["duree_minutes"] / 60

chart = alt.Chart(temps_par_mois).mark_line(point=True).encode(
    x=alt.X("mois:O", title="Mois", sort="ascending"),
    y=alt.Y("heures:Q", title="Temps total (heures)"),
    tooltip=[
        alt.Tooltip("mois:O", title="Mois"),
        alt.Tooltip("heures:Q", title="Heures", format=".1f")
    ]
)

st.altair_chart(chart, use_container_width=True)
# Répartition musculaire
volume_muscles = (
    workouts
    .groupby("muscle")["volume"]
    .sum()
    .reset_index()
)

# Suppression des muscles inconnus
volume_muscles = volume_muscles.dropna()

# Calcul du pourcentage
volume_muscles["pourcentage"] = (
    volume_muscles["volume"]
    / volume_muscles["volume"].sum()
    * 100
)


col_gauche, col_droite = st.columns([2, 1])

col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    st.subheader("Répartition musculaire")

    chart_muscles = alt.Chart(volume_muscles).mark_bar().encode(
        x=alt.X(
            "pourcentage:Q",
            title="Part du volume (%)"
        ),
        y=alt.Y(
            "muscle:N",
            title="Muscle",
            sort="-x"
        ),
        tooltip=[
            alt.Tooltip("muscle:N", title="Muscle"),
            alt.Tooltip(
                "pourcentage:Q",
                title="Pourcentage",
                format=".1f"
            ),
            alt.Tooltip(
                "volume:Q",
                title="Volume (kg)",
                format=",.0f"
            )
        ]
    )

    st.altair_chart(
        chart_muscles,
        use_container_width=True
    )

with col_droite:
        with col_droite:
        st.subheader("Temps d'entraînement")

        # Nombre de séries par muscle dans chaque séance
        temps_muscles = (
            workouts
            .dropna(subset=["muscle"])
            .groupby(["start_time", "muscle"])
            .size()
            .reset_index(name="nb_series")
        )

        # Nombre total de séries par séance
        total_series = (
            temps_muscles
            .groupby("start_time")["nb_series"]
            .sum()
            .reset_index(name="total_series")
        )

        # Ajout de la durée de séance
        temps_muscles = (
            temps_muscles
            .merge(total_series, on="start_time")
            .merge(
                sessions[["start_time", "duree_minutes"]],
                on="start_time"
            )
        )

        # Répartition de la durée
        temps_muscles["minutes"] = (
            temps_muscles["duree_minutes"]
            * temps_muscles["nb_series"]
            / temps_muscles["total_series"]
        )

        # Temps total par muscle
        temps_muscles = (
            temps_muscles
            .groupby("muscle", as_index=False)["minutes"]
            .sum()
            .sort_values("minutes", ascending=False)
        )

        chart_temps = alt.Chart(temps_muscles).mark_bar().encode(
            x=alt.X(
                "minutes:Q",
                title="Temps (min)"
            ),
            y=alt.Y(
                "muscle:N",
                sort="-x",
                title=""
            ),
            tooltip=[
                alt.Tooltip("muscle:N", title="Muscle"),
                alt.Tooltip("minutes:Q", title="Minutes", format=".0f")
            ]
        )

        st.altair_chart(
            chart_temps,
            use_container_width=True
        )




# Evolution de la charge moyenne par exercice

st.subheader("Évolution de la charge moyenne par exercice")


# Liste des exercices disponibles avec assez d'historique

exercices_valides = (
    workouts
    .dropna(subset=["weight_kg"])
    .groupby("exercise_title")["start_time"]
    .nunique()
    .reset_index(name="nombre_seances")
)

# Garder uniquement les exercices présents dans au moins 2 séances différentes

exercices_valides = exercices_valides[
    exercices_valides["nombre_seances"] >= 2
]


liste_exercices = (
    exercices_valides["exercise_title"]
    .sort_values()
    .tolist()
)


# Sélecteur d'exercice

exercice_selectionne = st.selectbox(
    "Choisir un exercice",
    liste_exercices
)


# Filtrer l'exercice choisi

evolution_exercice = workouts[
    workouts["exercise_title"] == exercice_selectionne
].copy()


# Supprimer les lignes sans charge

evolution_exercice = evolution_exercice.dropna(
    subset=["weight_kg"]
)


# Calcul de la charge moyenne par séance

evolution_exercice = (
    evolution_exercice
    .groupby("start_time", as_index=False)
    .agg(
        charge_moyenne=("weight_kg", "mean"),
        nombre_series=("set_index", "count")
    )
)


# Trier par date

evolution_exercice = evolution_exercice.sort_values(
    "start_time"
)


# Graphique

chart_evolution = alt.Chart(
    evolution_exercice
).mark_line(point=True).encode(

    x=alt.X(
        "start_time:T",
        title="Date"
    ),

    y=alt.Y(
        "charge_moyenne:Q",
        title="Charge moyenne (kg)"
    ),

    tooltip=[
        alt.Tooltip(
            "start_time:T",
            title="Date"
        ),
        alt.Tooltip(
            "charge_moyenne:Q",
            title="Charge moyenne",
            format=".1f"
        ),
        alt.Tooltip(
            "nombre_series:Q",
            title="Nombre de séries"
        )
    ]
)


st.altair_chart(
    chart_evolution,
    use_container_width=True
)


# -----------------------------
# Données brutes
# -----------------------------

st.divider()

st.subheader("Tableau des données brutes (workouts)")

st.dataframe(
    workouts,
    use_container_width=True
)