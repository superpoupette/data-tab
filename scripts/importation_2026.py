import pandas as pd


def load_danse():

    danse = pd.read_excel(
        "data/2026.xlsx",
        sheet_name="DANSE",
        engine="openpyxl"
    )

    return danse



def clean_danses_2026():

    danse = load_danse()


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


    # ==========================
    # Format final Google Sheet
    # ==========================

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




def load_2026():

    data2026 = pd.read_excel(
        "data/2026.xlsx",
        sheet_name="DATA",
        engine="openpyxl"
    )

    return data2026



def clean_2026(data2026):

    # Conversion de la date
    data2026["Date"] = pd.to_datetime(
        data2026["Date"],
        errors="coerce"
    )

    return data2026



def prepare_2026():

    data2026 = load_2026()
    data2026 = clean_2026(data2026)

    return data2026