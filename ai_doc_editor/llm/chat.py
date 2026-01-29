import sqlite3

DB_PATH = "database.db"

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

def chat_with_llm(session_id, user_query):
    save_message(session_id, "user", user_query)

    history = get_conversation(session_id)

    # 🔹 Placeholder LLM logic (replace later)
    response = f"Understood. I will apply: '{user_query}'"

    save_message(session_id, "ai", response)
    return response
