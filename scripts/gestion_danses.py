import pandas as pd

def load_danses(filepath):

    danses_recap = pd.read_csv(filepath)

    # Séparation artiste / titre / chorégraphe
    split = danses_recap["Nom"].str.split(
        " - ",
        n=2,
        expand=True
    )

    danses_recap["artiste"] = split[0]
    danses_recap["titre"] = split[1]
    danses_recap["choregraphe"] = split[2].fillna("")

    # Suppression colonne originale
    danses_recap = danses_recap.drop(
        columns=["Nom"]
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
        "Style",
        "Durée (s)",
        "Difficultée",
        "Estimation",
        "Note"
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

                morceaux_split = str(morceau).split(" - ", 2)

                artiste = morceaux_split[0]
                titre = morceaux_split[1] if len(morceaux_split) > 1 else ""
                choregraphe = morceaux_split[2] if len(morceaux_split) > 2 else ""

                lignes.append({
                    "date": row["Date"],
                    "annee": row["Date"].year,
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

    danse_2024 = clean_danse_recap(danse_2024)
    danse_2025 = clean_danse_recap(danse_2025)

    danse_recap = pd.concat(
        [
            danse_2024,
            danse_2025
        ],
        ignore_index=True
    )

    # Suppression doublons
    danse_recap = danse_recap.drop_duplicates(
        subset=[
            "artiste",
            "titre"
        ]
    )

    # Ajout du temps d'apprentissage
    duree_apprentissage = (
        danse_data
        .groupby(
            [
                "artiste",
                "titre"
            ],
            as_index=False
        )["duree_min"]
        .sum()
        .rename(
            columns={
                "duree_min": "duree_apprentissage"
            }
        )
    )

    danse_recap = danse_recap.merge(
        duree_apprentissage,
        on=[
            "artiste",
            "titre"
        ],
        how="left"
    )

    danse_recap["duree_apprentissage"] = (
        danse_recap["duree_apprentissage"]
        .fillna(0)
    )

    danse_recap = danse_recap[
        [
            "artiste",
            "titre",
            "choregraphe",
            "duree_apprentissage",
            "Style",
            "Durée (s)",
            "Difficultée",
            "Estimation",
            "Note"
        ]
    ]

    return danse_recap
