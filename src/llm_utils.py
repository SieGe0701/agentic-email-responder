import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("GEMINI_API_KEY:", GEMINI_API_KEY)


# Initialize LangChain Gemini model
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0, google_api_key=GEMINI_API_KEY)
# Prompt template
prompt_template = ChatPromptTemplate.from_template("""
You are an email assistant.
Task:
1. Summarize the following email in 3 sentences.
2. Draft a polite reply in the same language.

Email:
{email_text}
""")

def summarize_and_reply(email_text: str) -> dict:
    """
    Summarizes an email and drafts a reply using LangChain with Gemini.
    """
    chain = prompt_template | llm
    response = chain.invoke({"email_text": email_text})

    result = response.content.strip()

    # Try to split into summary/reply
    if "Reply:" in result:
        parts = result.split("Reply:")
        summary = parts[0].strip()
        reply = parts[1].strip()
    else:
        summary = result
        reply = "No reply generated."

    return {"summary": summary, "reply": reply}

def main():
    sample_email = """
    Hi Srinivas, 
    
    I wanted to remind you about our meeting scheduled for tomorrow at 3 PM. 
    Please let me know if you’re still available or if we need to reschedule.
    
    Best, 
    John
    """

    print("---- Testing Email Processor ----")
    result = summarize_and_reply(sample_email)
    print("Summary:\n", result["summary"])
    print("\nReply:\n", result["reply"])

if __name__ == "__main__":
    main()
