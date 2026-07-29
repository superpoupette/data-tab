import pandas as pd
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
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



def load_excel_from_drive(
    file_id,
    sheet_name
):

    service = get_drive_service()


    request = service.files().get_media(
        fileId=file_id
    )


    file = io.BytesIO()

    downloader = MediaIoBaseDownload(
        file,
        request
    )


    done = False

    while not done:

        status, done = downloader.next_chunk()


    file.seek(0)


    return pd.read_excel(
        file,
        sheet_name=sheet_name,
        engine="openpyxl"
    )



def load_csv_from_drive(
    file_id,
    separator=",",
    encoding="utf-8"
):

    url = (
        f"https://drive.google.com/uc?id={file_id}"
        "&export=download"
    )


    response = requests.get(url)

    response.raise_for_status()


    data = response.content.decode(
        encoding,
        errors="replace"
    )


    df = pd.read_csv(
        StringIO(data),
        sep=separator
    )


    return df