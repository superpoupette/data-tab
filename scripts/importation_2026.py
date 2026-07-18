import pandas as pd


def load_danse():

    danse = pd.read_excel(
        "data/2026.xlsx",
        sheet_name="DANSE"
    )

    return danse

def clean_danses_2026():

    danses = load_danses_2026()

    split = danses["Nom"].str.split(
        r"\s*-\s*",
        n=2,
        expand=True
    )

    danses["artiste"] = split[0]
    danses["titre"] = split[1].fillna("")
    danses["choregraphe"] = split[2].fillna("")

    danses = danses.rename(
        columns={
            "Style": "style",
            "Durée (s)": "duree",
            "Temps apprentissage (m)": "duree_apprentissage"
        }
    )

    danses["nombre_seance"] = None
    danses["duree_seance"] = None
    danses["date_debut"] = None
    danses["date_fin"] = None
    danses["difficulte"] = None
    danses["estimation"] = None
    danses["note"] = None
    danses["statut"] = "en cours"

    return danses[
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