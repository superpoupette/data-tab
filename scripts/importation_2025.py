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

    data2025 = data2025.rename(
        columns={
            "Chorée1_durée": "Choree1_duree",
            "Chorée2_durée": "Choree2_duree",
            "Chorée3_durée": "Choree3_duree",
            "Chorée4_durée": "Choree4_duree",
            "Chorée5_durée": "Choree5_duree",

            "Chorée1_morceau": "Choree1_morceau",
            "Chorée2_morceau": "Choree2_morceau",
            "Chorée3_morceau": "Choree3_morceau",
            "Chorée4_morceau": "Choree4_morceau",
            "Chorée5_morceau": "Choree5_morceau",
        }
    )
    return data2025


def prepare_2025(filepath):
    data2025 = load_csv(filepath)
    data2025 = clean_csv(data2025)

    return data2025