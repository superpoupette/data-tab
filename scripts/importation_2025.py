import pandas as pd


import pandas as pd


def load_csv(filepath):
    data2025 = pd.read_csv(filepath)
    return data2025


def clean_csv(data2025):

    data2025["Date"] = pd.to_datetime(
        data2025["Date"] + "/2025",
        format="%d/%m/%Y"
    )

    for col in ["Muscu_zone", "Muscu_zone2"]:
        data2025[col] = (
            data2025[col]
            .str.strip()
            .replace("💪", "bras")
            .replace("🍫", "abdos")
            .replace("🕺", "fullbody")
            .replace("🍑", "fesses")
            .replace("🦵", "jambes")
        )

    return data2025

def create_danse(data2025):

    lignes = []

    for _, row in data2025.iterrows():
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
                    "semaine": row["Semaine"],
                    "artiste": artiste,
                    "titre": titre,
                    "choregraphe": choregraphe,
                    "duree_min": duree
                })

    danse = pd.DataFrame(lignes)

    return danse


def prepare_2025(filepath):
    data2025 = load_csv(filepath)
    data2025 = clean_csv(data2025)
    danse = create_danse(data2025)

    return data2025, danse