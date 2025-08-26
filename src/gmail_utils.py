from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64
import os
import re
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail API scope for reading + modifying messages
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def get_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def get_unread_emails(max_results=5):
    service = get_service()
    results = service.users().messages().list(
        userId="me", labelIds=["UNREAD"], maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
        payload = msg_data.get("payload", {})
        headers = payload.get("headers", [])
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown Sender)")

        # Extract email body (text/plain or strip HTML if only html exists)
        body = ""
        def extract_parts(parts):
            for part in parts:
                if part["mimeType"] == "text/plain" and "data" in part["body"]:
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                elif part["mimeType"] == "text/html" and "data" in part["body"]:
                    html = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
                    return re.sub("<[^<]+?>", "", html)  # strip tags
                elif "parts" in part:
                    return extract_parts(part["parts"])
            return ""

        if "data" in payload.get("body", {}):
            body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
        elif "parts" in payload:
            body = extract_parts(payload["parts"])

        emails.append({"id": msg["id"], "subject": subject, "from": sender, "body": body})

    return emails


def mark_as_read(msg_id):
    service = get_service()
    service.users().messages().modify(
        userId="me", id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def send_email(to, subject, body_text):
    service = get_service()
    message = MIMEText(body_text)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message = {"raw": raw}
    sent = service.users().messages().send(userId="me", body=message).execute()
    return sent


if __name__ == "__main__":
    emails = get_unread_emails(max_results=5)
    for e in emails:
        print("=" * 50)
        print(f"From: {e['from']}")
        print(f"Subject: {e['subject']}")
        print(f"Body: {e['body'][:200]}...")  # first 200 chars
        # Example: mark email as read
        mark_as_read(e["id"])
        # Example: send a reply (you can comment this out if not needed)
        send_email(e["from"], f"Re: {e['subject']}", "Thanks for your email! This is an automated reply.")
