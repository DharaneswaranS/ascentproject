import sqlite3
import os
import requests
from llm.editor import apply_edit
from utils.versioning import save_new_version

DB_PATH = "database.db"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not set")

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# ---------------- DB HELPERS ---------------- #

def save_message(session_id, role, message):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO chat_memory (session_id, role, message) VALUES (?, ?, ?)",
        (session_id, role, message)
    )
    conn.commit()
    conn.close()

def get_conversation(session_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT role, message FROM chat_memory WHERE session_id=? ORDER BY id",
        (session_id,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows

def load_document_text():
    with open("outputs/extracted.txt", "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

# ---------------- MAIN CHAT ---------------- #

def chat_with_llm(session_id, user_query):
    save_message(session_id, "user", user_query)

    # 🔹 EDIT INTENT FIRST (IMPORTANT)
    edit_keywords = ["rewrite", "modify", "change", "improve", "make it"]

    if any(k in user_query.lower() for k in edit_keywords):
        try:
            base_text = load_document_text()
            edited_text = apply_edit(user_query, base_text)
            save_new_version(edited_text)

            reply = "✅ Document updated based on your instruction."
            save_message(session_id, "ai", reply)
            return reply

        except Exception as e:
            error_msg = f"❌ Document edit failed: {str(e)}"
            save_message(session_id, "ai", error_msg)
            return error_msg

    # 🔹 NORMAL CHAT FLOW
    history = get_conversation(session_id)
    document_text = load_document_text()

    messages = [
        {
            "role": "system",
            "content": (
                "You are an AI document assistant. "
                "Answer ONLY using the provided document content. "
                "If information is missing, say so."
            )
        },
        {
            "role": "system",
            "content": f"DOCUMENT CONTENT:\n{document_text[:6000]}"
        }
    ]

    for role, msg in history:
        messages.append({
            "role": "assistant" if role == "ai" else "user",
            "content": msg
        })

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.3
    }

    response = requests.post(
        GROQ_URL,
        headers=HEADERS,
        json=payload,
        timeout=60
    )

    data = response.json()

    if "choices" not in data:
        raise RuntimeError(f"GROQ CHAT ERROR: {data}")

    ai_reply = data["choices"][0]["message"]["content"]
    save_message(session_id, "ai", ai_reply)
    return ai_reply
