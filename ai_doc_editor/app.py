from flask import Flask, render_template, request, jsonify, session
import os, uuid

from ocr.preprocess import preprocess_image
from ocr.validate import validate_document
from ocr.extract import extract_text
from llm.chat import chat_with_llm

app = Flask(__name__)
app.secret_key = "doc-secret"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        processed_path = preprocess_image(path)

        is_valid, conf = validate_document(processed_path)
        if not is_valid:
            return jsonify({
                "status": "rejected",
                "message": "Unreadable document"
            })

        extract_text(processed_path)
        session["session_id"] = str(uuid.uuid4())

        return jsonify({
            "status": "accepted",
            "message": "Document accepted. Start chatting."
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json["query"]
    session_id = session.get("session_id")

    response = chat_with_llm(session_id, user_query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
