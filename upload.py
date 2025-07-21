import os
import pickle
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_youtube(file_path, title):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Load client secret from ENV
    client_secret_str = os.environ["CLIENT_SECRET_JSON"]
    client_secret = json.loads(client_secret_str)

    # Auth flow
    flow = InstalledAppFlow.from_client_config(client_secret, scopes)
    credentials = flow.run_local_server()

    with open("token.pkl", "wb") as f:
        pickle.dump(credentials, f)

    youtube = build("youtube", "v3", credentials=credentials)

    request_body = {
        "snippet": {
            "title": title[:100],
            "description": "Generated using AI and DeepSeek",
            "tags": ["ai", "reddit", "shorts"],
            "categoryId": "24"
        },
        "status": {
            "privacyStatus": "public",
            "madeForKids": False
        }
    }

    media_file = MediaFileUpload(file_path)
    response = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    ).execute()

    print("✅ Uploaded:", response["id"])
