import pandas as pd

def load_tv(filepath):
    tv = pd.read_csv(filepath)
    return tv


def tab_tv():
    tv=load_tv("data/tvtime.csv")
    return tv
