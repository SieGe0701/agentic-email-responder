# filters.py
import os, json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY"),
)

# Few-shot style classification prompt
prompt = ChatPromptTemplate.from_template(
    """Classify the email into exactly one of: "spam", "important", or "neutral".

Definitions:
- spam: promotional/marketing, phishing/scam, bulk outreach, or unwanted newsletter.
- important: likely requires my response/action (work/personal coordination, scheduling, questions, approvals).
- neutral: transactional notifications, OTPs, receipts, newsletters worth keeping but no reply needed.

Return your response as a **valid JSON object only**, in this exact format:

{{
  "label": "spam|important|neutral",
  "confidence": 0.0-1.0,
  "reasons": "short explanation of why you chose this category"
}}

Do not include any extra text, explanations, or markdown. Only return the JSON.

Examples:

From: "scammer@bad.com"
Subject: "You won a FREE iPhone!"
Body: "Click here to claim your prize"
Output: {{"label": "spam", "confidence": 0.95, "reasons": ["too good to be true", "phishing style"]}}

From: "colleague@work.com"
Subject: "Meeting agenda for tomorrow"
Body: "Please find attached the agenda for tomorrow's project meeting"
Output: {{"label": "important", "confidence": 0.92, "reasons": ["work-related", "requires action"]}}

From: "no-reply@bank.com"
Subject: "Your monthly account statement"
Body: "Attached is your statement for July"
Output: {{"label": "neutral", "confidence": 0.88, "reasons": ["transactional notification"]}}

Now classify this one:

From: {sender}
Subject: {subject}
Body:
{body}
"""
)

def classify_email(subject: str, sender: str, body: str):
    """
    Calls Gemini to classify an email into spam, important, or neutral.
    Returns dict: {label, confidence, reasons}.
    """
    chain = prompt | llm
    resp = chain.invoke({
        "sender": sender or "",
        "subject": subject or "",
        "body": body or ""
    })
    text = (resp.content or "").strip()

    try:
        data = json.loads(text)
        label = (data.get("label") or "").lower().strip()
        if label not in ("spam", "important", "neutral"):
            label = "neutral"
        conf = float(data.get("confidence", 0.6))
        reasons = data.get("reasons") or []
        return {"label": label, "confidence": conf, "reasons": reasons}
    except Exception:
        # Fallback parsing if the model didn’t return valid JSON
        lowered = text.lower()
        if "spam" in lowered:
            label = "spam"
        elif "important" in lowered:
            label = "important"
        else:
            label = "neutral"
        return {"label": label, "confidence": 0.6, "reasons": ["fallback_parse"]}

