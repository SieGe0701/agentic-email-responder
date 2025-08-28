# Main entry point for the Agentic AI Email Responder
from gmail_utils import get_unread_emails, send_reply
from llm_utils import summarize_email, draft_reply

def main():
	print("Fetching unread emails...")
	emails = get_unread_emails()
	for email in emails:
		print(f"\nFrom: {email['from']}")
		print(f"Subject: {email['subject']}")
		summary = summarize_email(email['body'])
		print(f"Summary: {summary}")
		reply = draft_reply(summary, email)
		print(f"Drafted Reply: {reply}")
		# Uncomment to send reply automatically
		# send_reply(email, reply)

if __name__ == "__main__":
	main()
