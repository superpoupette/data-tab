import pandas as pd



def clean_danses_2026(danse):


    # ==========================
    # Séparation Nom
    # ==========================

    split = danse["Nom"].str.split(
        r"\s*-\s*",
        n=2,
        expand=True
    )

    danse["artiste"] = split[0]

    danse["titre"] = (
        split[1]
        if 1 in split.columns
        else ""
    )

    danse["choregraphe"] = (
        split[2]
        if 2 in split.columns
        else ""
    )


    # ==========================
    # Renommage colonnes
    # ==========================

    danse = danse.rename(
        columns={
            "Style": "style",
            "Durée (s)": "duree",
            "Temps apprentissage (m)": "duree_apprentissage"
        }
    )


    # ==========================
    # Colonnes absentes
    # ==========================

    danse["date_debut"] = ""
    danse["date_fin"] = ""

    danse["nombre_seance"] = ""
    danse["duree_seance"] = ""

    danse["difficulte"] = ""
    danse["estimation"] = ""
    danse["note"] = ""

    danse["statut"] = "en cours"


    # ==========================
    # Nettoyage
    # ==========================

    danse = danse.drop(
        columns=[
            "Nom",
            "Temps par minute (m)",
            "Temps par minute (h)"
        ],
        errors="ignore"
    )


    colonnes = [
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


    for col in colonnes:

        if col not in danse.columns:
            danse[col] = ""


    danse = danse[colonnes]


    return danse




def clean_2026(data2026):


    # Nettoyage noms colonnes

    data2026.columns = (
        data2026.columns
        .astype(str)
        .str.strip()
    )


    # La colonne "/" contient les dates

    data2026 = data2026.rename(
        columns={
            "/": "Date"
        }
    )


    data2026["Date"] = pd.to_datetime(
        data2026["Date"],
        errors="coerce"
    )


    return data2026