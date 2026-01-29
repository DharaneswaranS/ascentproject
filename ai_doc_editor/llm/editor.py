import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "YOUR_KEY_HERE"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def apply_edit(instruction, current_text):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI document editor. "
                "Apply the user's instruction strictly to the document text. "
                "Return ONLY the edited document text."
            )
        },
        {
            "role": "user",
            "content": f"DOCUMENT:\n{current_text}\n\nINSTRUCTION:\n{instruction}"
        }
    ]

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.2
    }

    res = requests.post(GROQ_URL, headers=HEADERS, json=payload)
    return res.json()["choices"][0]["message"]["content"]
