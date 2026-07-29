from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import pandas as pd
import io
import streamlit as st


def get_drive_service():

    credentials = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=[
            "https://www.googleapis.com/auth/drive.readonly"
        ]
    )

    service = build(
        "drive",
        "v3",
        credentials=credentials
    )

    return service



def load_csv_from_drive(
    file_id,
    separator=";"
):

    service = get_drive_service()

    request = service.files().get_media(
        fileId=file_id
    )

    content = request.execute()

    df = pd.read_csv(
        io.BytesIO(content),
        sep=separator,
        encoding="utf-8-sig"
    )

    return df