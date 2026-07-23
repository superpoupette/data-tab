import pandas as pd


def load_workouts(filepath):
    workouts = pd.read_csv(filepath)
    return workouts


def load_exercices(filepath):
    exercices = pd.read_csv(filepath, sep=";")
    return exercices


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

        workouts["start_time"] = (
            workouts["start_time"]
            .astype(str)
            .str.replace(fr, en, regex=False)
        )

        workouts["end_time"] = (
            workouts["end_time"]
            .astype(str)
            .str.replace(fr, en, regex=False)
        )


    workouts["start_time"] = pd.to_datetime(
        workouts["start_time"],
        format="%d %b %Y, %H:%M",
        errors="coerce"
    )

    workouts["end_time"] = pd.to_datetime(
        workouts["end_time"],
        format="%d %b %Y, %H:%M",
        errors="coerce"
    )

    return workouts



def add_volume(workouts):

    workouts["volume"] = (
        pd.to_numeric(workouts["weight_kg"], errors="coerce")
        *
        pd.to_numeric(workouts["reps"], errors="coerce")
    )

    return workouts



def create_sessions(workouts):

    sessions = (
        workouts
        .dropna(
            subset=[
                "start_time",
                "end_time"
            ]
        )
        .groupby("start_time")
        .agg(
            end_time=("end_time", "first"),
            nombre_series=("set_index", "count"),
            nombre_exercices=("exercise_title", "nunique"),
            volume_total=("volume", "sum"),
        )
        .reset_index()
    )


    # Durée de séance en minutes

    sessions["duree_minutes"] = (
        (
            sessions["end_time"]
            -
            sessions["start_time"]
        )
        .dt.total_seconds()
        /
        60
    )


    # Date sans l'heure
    sessions["Date"] = (
        sessions["start_time"]
        .dt.normalize()
    )


    return sessions



def prepare_data(workouts_filepath, exercices_filepath=None):

    workouts = load_workouts(workouts_filepath)

    workouts = clean_dates(workouts)

    workouts = add_volume(workouts)


    sessions = create_sessions(workouts)


    return workouts, sessions