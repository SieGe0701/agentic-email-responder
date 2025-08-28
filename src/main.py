from gmail_utils import get_unread_emails,mark_as_read,send_email
from llm_utils import summarize_and_reply

def main():
    print("---- Fetching unread emails ----")
    emails = get_unread_emails(max_results=3)  # limit for testing
    
    if not emails:
        print("No unread emails found.")
        return

    for idx, email in enumerate(emails, start=1):
        print(f"\n===== Email {idx} =====")
        print("From:", email["from"])
        print("Subject:", email["subject"])
        print("Body:\n", email["body"][:500], "...")  # preview
        mark_as_read(email["id"])

        # Run LLM processing
        result = summarize_and_reply(email["body"])
        print("\n--- LLM Output ---")
        print("Summary:\n", result["summary"])
        print("\nReply:\n", result["reply"])
        send_email(email["from"], f"Re: {email['subject']}", result["reply"])

if __name__ == "__main__":
    main()
