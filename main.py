from scripts.importation_hevy import prepare_data
from scripts.importation_babelio import prepare_babelio
from scripts.importation_2025 import prepare_2025


workouts, sessions = prepare_data(
    "data/workouts.csv","data/exercices.csv"
)

livres = prepare_babelio(
    "data/biblio.csv"
)

data2025 = prepare_2025(
    "data/2025.csv"
)

print(data2025.head())