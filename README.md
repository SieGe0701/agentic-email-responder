# Email Summarizer + Auto-Responder

This project uses Gmail API + a Large Language Model (via LangChain) to:
- Fetch unread emails
- Summarize them in a few sentences
- Draft a polite reply automatically

---

## Setup
1. Create virtual environment:
   `powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   `

2. Add your **API key** to .env:
   `
   GEMINI_API_KEY=your_key_here
   `
   (Alternatively, replace with Gemini Groq/Hugging Face TogetherAI depending on provider.)

3. Enable Gmail API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Gmail API for your project
   - Download credentials.json and place it in the project root
   - Run initial auth flow to generate 	oken.json

4. Run the project:
   `powershell
   python src\main.py
   `

---


## Project Structure

```
agentic-email-responder/
├── .gitignore
├── README.md
├── requirements.txt
├── credentials.json         # (to be added manually, if using Gmail API)
├── token.json               # (if using Gmail API OAuth)
├── data/                    # Store cached emails (optional, currently empty)
├── logs/                    # Log files (optional, currently empty)
├── src/
│   ├── main.py              # Entry point
│   ├── gmail_utils.py       # IMAP/SMTP (and optional Gmail API) functions
│   ├── llm_utils.py         # LLM summarization + reply
│   └── .env                 # API keys and secrets (Gemini, email, etc.)
└── venv/                    # Virtual environment (not tracked by git)
```

---

## Next Steps
- Add approval step before sending replies
- Swap in open-source models (Groq, TogetherAI, Hugging Face) if desired
- Extend agent logic (e.g., ignore spam, auto-confirm meetings)
