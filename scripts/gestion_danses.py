import pandas as pd

def load_danses(filepath):
    danses_recap = pd.read_csv(filepath)

    split = danses_recap["Nom"].str.split(
        " - ",
        n=2,
        expand=True
    )

    danses_recap["artiste"] = split[0]
    danses_recap["titre"] = split[1]
    danses_recap["choregraphe"] = split[2].fillna("")

    danses_recap = danses_recap.drop(columns=["Nom"])

    danses_recap = danses_recap.dropna(how="all")

    return danses_recap

def create_danse_data(data):

    lignes = []

    for _, row in data.iterrows():
        for i in range(1, 6):
            morceau = row[f"Chorée{i}_morceau"]
            duree = pd.to_numeric(
                row[f"Chorée{i}_durée"],
                errors="coerce"
            )

            if pd.notna(morceau):
                morceaux_split = str(morceau).split(" - ", 2)

                artiste = morceaux_split[0]
                titre = morceaux_split[1] if len(morceaux_split) > 1 else ""
                choregraphe = morceaux_split[2] if len(morceaux_split) > 2 else ""

                lignes.append({
                    "date": row["Date"],
                    "artiste": artiste,
                    "titre": titre,
                    "choregraphe": choregraphe,
                    "duree_min": duree
                })

    danse_data = pd.DataFrame(lignes)

    return danse_data


def create_danse_recap(danse_data):
    danse_recap = load_danses("data/danses_2025.csv")

    # Calcul du temps total d'apprentissage par chorégraphie
    duree_apprentissage = (
        danse_data
        .groupby(["artiste", "titre"], as_index=False)["duree_min"]
        .sum()
        .rename(
            columns={
                "duree_min": "duree_apprentissage"
            }
        )
    )

    # Ajout dans le tableau récapitulatif
    danse_recap = danse_recap.merge(
        duree_apprentissage,
        on=["artiste", "titre"],
        how="left"
    )

    # Remplace les valeurs absentes par 0
    danse_recap["duree_apprentissage"] = (
        danse_recap["duree_apprentissage"]
        .fillna(0)
    )

    # Réorganisation des colonnes
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
