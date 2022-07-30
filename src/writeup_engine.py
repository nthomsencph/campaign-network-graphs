# imports
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build

from markdownify import markdownify
import io
from pathlib import Path
import re


SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.metadata",
]


class GDocHandler:
    def __init__(self, json_key) -> None:

        self.creds = Credentials.from_service_account_file(
            json_key, scopes=SCOPES
        )

    def init_service(self):

        self.service = build("drive", "v3", credentials=self.creds)
        return self

    def export_to_markdown(
        self, file_id=None, path="local_storage/writeup.md"
    ):

        assert file_id or self.gdoc_fields.get("id"), "Need ID to export!"

        request = self.service.files().export_media(
            fileId=file_id if file_id else self.gdoc_fields.get("id"),
            mimeType="text/html",
        )
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            _, done = downloader.next_chunk()

        Path(path).write_text(self.preprocess_md(markdownify(fh.getvalue())))

    def get_file_info(self, file_id=None, file_title=None):
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        Include ', exportLinks' in fields to see possible export formats
        for files.
        """

        assert file_id or file_title, "FileID or title needed!"

        if file_id:
            results = (
                self.service.files()
                .get(
                    fileId=file_id,
                    fields="id, name, version, owners",
                )
                .execute()
            )

        else:
            results = (
                self.service.files()
                .list(
                    fields="id, name, version, owners",
                )
                .execute()
                .get("files")
            )

            results = next(x for x in results if x["name"] == file_title)

        self.gdoc_fields = results
        return self.gdoc_fields

    def preprocess_md(self, md, img_dims=(600, 400)):

        w, h = img_dims
        md = "# " + md[md.find("A Tale of Damnation") :]
        p = re.compile(r"\!\[\]\((.+)\)")
        return p.sub(
            rf' <img src="\1" width="{w}" height="{h}" /> ', md
        ).replace("\\", "")
