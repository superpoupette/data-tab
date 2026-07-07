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


def prepare_2025(filepath):
    data2025 = load_csv(filepath)
    data2025 = clean_csv(data2025)

    return data2025