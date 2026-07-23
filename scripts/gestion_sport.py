import pandas as pd

COLONNES_SPORT = [
    "Date",
    "Danse",
    "Muscu",
    "Stretching",
    "Course",
    "Escalade",
    "Randonnée",
    "Autre",
]

def charger_tableau_sport():
    """Retourne le tableau de suivi sportif."""
    df = pd.DataFrame(columns=COLONNES_SPORT)
    return df