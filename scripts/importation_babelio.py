import pandas as pd

def load_babelio(filepath):
    livres = pd.read_csv(
        filepath,
        sep=";",
        encoding="cp1252",
        quotechar='"'
    )
    return livres

def prepare_babelio(filepath):
    livres = load_babelio(filepath)
    return livres
