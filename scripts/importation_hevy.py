import pandas as pd


def load_workouts(filepath):
    workouts = pd.read_csv(filepath)
    return workouts


def clean_dates(workouts):
    mois = {
        "janv.": "Jan",
        "févr.": "Feb",
        "mars": "Mar",
        "avr.": "Apr",
        "mai": "May",
        "juin": "Jun",
        "juil.": "Jul",
        "août": "Aug",
        "sept.": "Sep",
        "oct.": "Oct",
        "nov.": "Nov",
        "déc.": "Dec"
    }

    for fr, en in mois.items():
        workouts["start_time"] = workouts["start_time"].str.replace(fr, en)

    workouts["start_time"] = pd.to_datetime(
        workouts["start_time"],
        format="%d %b %Y, %H:%M"
    )

    return workouts


def add_volume(workouts):
    workouts["volume"] = (
        workouts["weight_kg"] * workouts["reps"]
    )

    return workouts


def create_sessions(workouts):
    sessions = workouts.groupby("start_time").agg(
        nombre_series=("set_index", "count"),
        nombre_exercices=("exercise_title", "nunique"),
        volume_total=("volume", "sum")
    )

    sessions = sessions.reset_index()

    return sessions

def prepare_data(filepath):
    workouts = load_workouts(filepath)
    workouts = clean_dates(workouts)
    workouts = add_volume(workouts)
    sessions = create_sessions(workouts)
    return workouts, sessions
