import pandas as pd


def load_workouts(filepath):
    return pd.read_csv(filepath)



def load_exercices(filepath):
    return pd.read_csv(filepath, sep=";")



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
        pd.to_numeric(
            workouts["weight_kg"],
            errors="coerce"
        )
        *
        pd.to_numeric(
            workouts["reps"],
            errors="coerce"
        )
    )

    return workouts



def add_muscle(workouts, exercices):

    workouts = workouts.merge(
        exercices[
            [
                "exercise_title",
                "muscle"
            ]
        ],
        on="exercise_title",
        how="left"
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


    sessions["mois"] = (
        sessions["start_time"]
        .dt.to_period("M")
    )


    return sessions

def replace_exercise_title(workouts):

    # Lignes où les notes ne sont pas vides
    masque = (
        workouts["exercise_notes"].notna()
        &
        (workouts["exercise_notes"].str.strip() != "")
        &
        ~(
            (workouts["exercise_title"] == "Hip Thrust (Barbell)")
            &
            (workouts["start_time"] == pd.Timestamp("2026-07-10 08:00:00"))
        )
    )

    # Remplacement
    workouts.loc[masque, "exercise_title"] = (
        workouts.loc[masque, "exercise_notes"]
    )

    return workouts


def prepare_data(
    workouts_filepath,
    exercices_filepath
):

    workouts = load_workouts(
        workouts_filepath
    )

    exercices = load_exercices(
        exercices_filepath
    )


    workouts = clean_dates(
        workouts
    )

    workouts = replace_exercise_title(
        workouts
    )

    workouts = add_volume(
        workouts
    )

    workouts = add_muscle(
        workouts,
        exercices
    )


    sessions = create_sessions(
        workouts
    )


    return workouts, sessions

