from flask import Flask, render_template, request, jsonify, session
from utils.versioning import get_latest_edited_text
from utils.pdf_generator import generate_pdf_from_text
from flask import send_file

import os, uuid

from ocr.preprocess import preprocess_image
from ocr.validate import validate_document
from ocr.extract import extract_text
from llm.chat import chat_with_llm

from passport.extractor import extract_passport_data
from passport.face_detector import detect_face
from passport.signature_detector import detect_signature
from passport.utils import pdf_to_image

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
@app.route("/download")
def download_pdf():
    text = get_latest_edited_text()
    if not text:
        return "No edited document available", 400

    pdf_path = "outputs/final.pdf"
    generate_pdf_from_text(text, pdf_path)

    return send_file(pdf_path, as_attachment=True)
@app.route("/passport", methods=["POST"])
def passport_handler():
    file = request.files["file"]
    path = os.path.join("uploads", file.filename)
    file.save(path)

    # Convert PDF to image if needed
    if path.lower().endswith(".pdf"):
        image_path = pdf_to_image(path)
    else:
        image_path = path

    passport_data = extract_passport_data(image_path)
    if not passport_data:
        return {
            "status": "FAILED",
            "reason": "MRZ not detected"
        }

    face_present = detect_face(image_path)
    signature_present = detect_signature(image_path)

    return {
        "status": "SUCCESS",
        "document_type": "PASSPORT",
        "passport_data": passport_data,
        "photo_present": face_present,
        "signature_present": signature_present,
        "valid": face_present and signature_present
    }
@app.route("/passport-ui")
def passport_ui():
    return render_template("passport.html")


if __name__ == "__main__":
    app.run(debug=True)
