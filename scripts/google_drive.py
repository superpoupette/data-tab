import pandas as pd
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import streamlit as st
import json

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
    separator=";",
    encoding="utf-8-sig"
):

    service = get_drive_service()

    request = service.files().get_media(
        fileId=file_id
    )

    content = request.execute()

    df = pd.read_csv(
        io.BytesIO(content),
        sep=separator,
        encoding=encoding
    )

    return df


def load_json_folder_from_drive(
    folder_id,
    filename_prefix=None
):

    service = get_drive_service()

    query = (
        f"'{folder_id}' in parents "
        "and trashed = false"
    )

    results = service.files().list(
        q=query,
        fields="files(id,name)"
    ).execute()

    fichiers = results.get(
        "files",
        []
    )

    if filename_prefix is not None:

        fichiers = [
            f
            for f in fichiers
            if f["name"].startswith(
                filename_prefix
            )
        ]

    fichiers = sorted(
        fichiers,
        key=lambda x: x["name"]
    )

    data = []

    for fichier in fichiers:

        request = service.files().get_media(
            fileId=fichier["id"]
        )

        content = request.execute()

        data.extend(
            json.loads(
                content.decode("utf-8")
            )
        )

    return data