# Create main project folders
New-Item -ItemType Directory "src"
New-Item -ItemType Directory "data"
New-Item -ItemType Directory "logs"

# Create Python starter files
New-Item -ItemType File "src\main.py"
New-Item -ItemType File "src\gmail_utils.py"
New-Item -ItemType File "src\llm_utils.py"

# Create requirements file
@"
langchain
langchain-openai
google-api-python-client
google-auth
google-auth-oauthlib
python-dotenv
"@ | Out-File -Encoding utf8 "requirements.txt"

# Create .env file for API keys (empty for now)
@"
OPENAI_API_KEY=
"@ | Out-File -Encoding utf8 ".env"

# Create README
@"
# Email Summarizer + Auto-Responder

This project uses Gmail API + a Large Language Model (via LangChain) to:
- Fetch unread emails
- Summarize them in a few sentences
- Draft a polite reply automatically

---

## Setup
1. Create virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Add your **API key** to `.env`:
   ```
   OPENAI_API_KEY=your_key_here
   ```
   (Alternatively, replace with Groq/Hugging Face TogetherAI depending on provider.)

3. Enable Gmail API:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Gmail API for your project
   - Download `credentials.json` and place it in the project root
   - Run initial auth flow to generate `token.json`

4. Run the project:
   ```powershell
   python src\main.py
   ```

---

## Project Structure
```
EmailResponder/
│── venv/                 # Virtual environment
│── src/
│   ├── main.py           # Entry point
│   ├── gmail_utils.py    # Gmail API functions
│   ├── llm_utils.py      # LLM summarization + reply
│── data/                 # Store cached emails
│── logs/                 # Log files
│── requirements.txt
│── .env
│── README.md
│── credentials.json      # (to be added manually)
│── token.json            # Generated after first login
```

---

## Next Steps
- Add approval step before sending replies
- Swap in open-source models (Groq, TogetherAI, Hugging Face) if desired
- Extend agent logic (e.g., ignore spam, auto-confirm meetings)
"@ | Out-File -Encoding utf8 "README.md"
