# -*- coding: utf-8 -*-

import pandas as pd

from scripts.importation_2026 import clean_danses_2026

def load_danses(filepath):

    danses_recap = pd.read_csv(filepath)

    # Séparation artiste / titre / chorégraphe
    split = danses_recap["Nom"].str.split(
        r"\s*-\s*",
        n=2,
        expand=True
    )

    danses_recap["artiste"] = split[0]

    danses_recap["titre"] = (
        split[1]
        if 1 in split.columns
        else ""
    )

    danses_recap["choregraphe"] = (
        split[2].fillna("")
        if 2 in split.columns
        else ""
    )

    # Suppression colonne originale
    danses_recap = danses_recap.drop(
        columns=["Nom"]
    )

    # Renommage des colonnes
    danses_recap = danses_recap.rename(
        columns={
            "Style": "style",
            "Durée (s)": "duree",
            "Difficultée": "difficulte",
            "Estimation": "estimation",
            "Note": "note"
        }
    )

    # Suppression lignes vides
    danses_recap = danses_recap.dropna(
        how="all"
    )

    return danses_recap


def clean_danse_recap(danses_recap):

    colonnes_attendues = [
        "artiste",
        "titre",
        "choregraphe",
        "date_debut",
        "date_fin",
        "duree_apprentissage",
        "nombre_seance",
        "duree_seance",
        "style",
        "duree",
        "difficulte",
        "estimation",
        "note",
        "statut"
    ]

    for col in colonnes_attendues:
        if col not in danses_recap.columns:
            danses_recap[col] = None

    return danses_recap[colonnes_attendues]


def create_danse_data(data):

    lignes = []

    for _, row in data.iterrows():

        for i in range(1, 6):

            morceau = row[f"Choree{i}_morceau"]

            duree = pd.to_numeric(
                row[f"Choree{i}_duree"],
                errors="coerce"
            )

            if pd.notna(morceau):

                morceaux_split = str(morceau).split(
                    " - ",
                    2
                )

                artiste = morceaux_split[0]
                titre = morceaux_split[1] if len(morceaux_split) > 1 else ""
                choregraphe = morceaux_split[2] if len(morceaux_split) > 2 else ""

                lignes.append({
                    "date": pd.to_datetime(row["Date"]),
                    "annee": pd.to_datetime(row["Date"]).year,
                    "artiste": artiste,
                    "titre": titre,
                    "choregraphe": choregraphe,
                    "duree_min": duree
                })

    danse_data = pd.DataFrame(lignes)

    return danse_data


def create_danse_recap(danse_data):

    danse_2024 = load_danses(
        "data/danses_2024.csv"
    )

    danse_2025 = load_danses(
        "data/danses_2025.csv"
    )

    danse_2024 = clean_danse_recap(
        danse_2024
    )

    danse_2025 = clean_danse_recap(
        danse_2025
    )

    danse_recap = pd.concat(
        [
            danse_2024,
            danse_2025
        ],
        ignore_index=True
    )
    # Sécurité : création des colonnes absentes
    colonnes_google_sheet = [
        "date_debut",
        "date_fin",
        "duree_apprentissage",
        "nombre_seance",
        "duree_seance",
        "statut"
    ]


    for col in colonnes_google_sheet:
        if col not in danse_recap.columns:
            danse_recap[col] = ""

    # Suppression des doublons
    danse_recap = danse_recap.drop_duplicates(
        subset=[
            "artiste",
            "titre"
        ]
    )


    # ==========================
    # Statistiques apprentissage
    # ==========================

    stats_apprentissage = (
        danse_data
        .groupby(
            [
                "artiste",
                "titre"
            ],
            as_index=False
        )
        .agg(
            duree_apprentissage=(
                "duree_min",
                "sum"
            ),
            nombre_seance=(
                "duree_min",
                "count"
            ),
            duree_seance=(
                "duree_min",
                "mean"
            )
        )
    )


    # ==========================
    # Dates apprentissage
    # ==========================

    dates = (
        danse_data
        .groupby(
            [
                "artiste",
                "titre"
            ],
            as_index=False
        )
        .agg(
            date_debut=(
                "date",
                "min"
            ),
            date_fin=(
                "date",
                "max"
            )
        )
    )


    danse_recap = danse_recap.merge(
        stats_apprentissage,
        on=[
            "artiste",
            "titre"
        ],
        how="left"
    )


    # suppression des anciennes statistiques
    danse_recap = danse_recap.drop(
        columns=[
            "duree_apprentissage",
            "nombre_seance",
            "duree_seance"
        ],
        errors="ignore"
    )


    danse_recap = danse_recap.merge(
        stats_apprentissage,
        on=[
            "artiste",
            "titre"
        ],
        how="left"
    )

    # Valeurs par défaut
    danse_recap["duree_apprentissage"] = (
        danse_recap["duree_apprentissage"]
        .fillna(0)
    )

    danse_recap["nombre_seance"] = (
        danse_recap["nombre_seance"]
        .fillna(0)
        .astype(int)
    )

    danse_recap["duree_seance"] = (
        danse_recap["duree_seance"]
        .fillna(0)
        .round(1)
    )


    # ==========================
    # Statut
    # ==========================

    today = pd.Timestamp.today().normalize()

    danse_recap["statut"] = (
        (
            today - pd.to_datetime(
                danse_recap["date_fin"]
            )
        ).dt.days <= 90
    )

    danse_recap["statut"] = danse_recap["statut"].map(
        {
            True: "en cours",
            False: "termine"
        }
    )


    # ==========================
    # Format dates
    # ==========================

    danse_recap["date_debut"] = pd.to_datetime(
        danse_recap["date_debut"]
    ).dt.strftime("%Y-%m-%d")


    danse_recap["date_fin"] = pd.to_datetime(
        danse_recap["date_fin"]
    ).dt.strftime("%Y-%m-%d")


    # ==========================
    # Colonnes finales
    # ==========================

    danse_recap = danse_recap[
        [
            "artiste",
            "titre",
            "choregraphe",
            "date_debut",
            "date_fin",
            "duree_apprentissage",
            "nombre_seance",
            "duree_seance",
            "style",
            "duree",
            "difficulte",
            "estimation",
            "note",
            "statut"
        ]
    ]


    return danse_recap