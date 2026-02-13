🧠 AI Document Reader & Passport Verification System

A Flask-based AI application that allows users to:

📄 Upload documents (PDF/Image)

💬 Chat with an AI strictly grounded on the uploaded document

✏️ Edit documents via natural language instructions

⬇️ Download the edited document as PDF

🛂 Verify passport documents by extracting data and checking authenticity signals

🚀 Features Overview
1️⃣ AI Document Chat & Editor

Upload a document (PDF/Image)

AI answers only from document content

Supports document editing instructions (rewrite, modify, improve, etc.)

Maintains chat history per session

Versioned document updates

Download final edited document as PDF

2️⃣ Passport Verification Module (Initial Version)

Upload passport image or PDF

Extract passport data using OCR + MRZ parsing

Detect presence of:

👤 Face photo

✍️ Signature

Return structured verification result

Simple validity decision logic
ai_doc_editor/
│
├── app.py                     # Main Flask application
│
├── llm/
│   └── chat.py                # LLM chat logic (Groq API)
│
├── passport/
│   ├── face_detector.py       # Face detection using OpenCV Haar Cascade
│   ├── signature_detector.py  # Signature presence detection
│   ├── mrz_extractor.py       # MRZ parsing & passport field extraction
│   └── utils.py               # PDF → image utilities
│
├── ocr/
│   ├── preprocess.py          # Image preprocessing
│   ├── extract.py             # OCR text extraction
│   └── validate.py            # Basic document validation
│
├── utils/
│   ├── versioning.py          # Document version control
│   └── pdf_generator.py       # Text → PDF generator
│
├── templates/
│   ├── index.html             # AI Document Chat UI
│   └── passport.html          # Passport Verification UI
│
├── static/
│   ├── style.css              # UI styles
│   └── script.js              # Frontend logic
│
├── uploads/                   # Uploaded files
├── outputs/                   # Extracted text & generated PDFs
└── database.db                # SQLite chat memory
Tech Stack

Backend: Flask (Python)

AI / LLM: Groq API (LLaMA 3.1)

OCR: Tesseract / initial OCR pipeline

Computer Vision: OpenCV

Database: SQLite

Frontend: HTML, CSS, JavaScript

PDF Handling: ReportLab / custom generator
Setup Instructions
1️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate   # Linux / Mac
.venv\Scripts\activate      # Windows

2️⃣ Install Dependencies
pip install flask opencv-python pytesseract requests reportlab


Make sure Tesseract OCR is installed and added to PATH.

3️⃣ Set Environment Variable (Groq API)
setx GROQ_API_KEY "your_groq_api_key"

4️⃣ Initialize Database
python db/init_db.py

5️⃣ Run Application
python app.py


Open:

http://127.0.0.1:5000

🧠 AI Chat Logic (Important)
AI cannot hallucinate

Responses are generated only from uploaded document text

Chat history is stored per session

Edits create a new document version

System prompt enforced:

"You are an AI document assistant.
Answer ONLY using the provided document content.
Do not hallucinate."
Passport Verification Logic 
Pipeline:

Upload passport image / PDF

Convert PDF → image if needed

OCR text extraction

MRZ parsing (name, passport no, nationality, DOB, expiry)

Face detection using Haar Cascades

Signature detection using ink-pixel analysis

Return verification result

Validity Rule:
valid = face_present and signature_present
Passport API Endpoint
POST /passport


Response Example:

{
  "status": "SUCCESS",
  "document_type": "PASSPORT",
  "passport_data": {
    "name": "BENJAMIN FRANKLIN",
    "passport_no": "575034801",
    "nationality": "USA",
    "dob": "170601",
    "expiry": "280115"
  },
  "photo_present": true,
  "signature_present": true,
  "valid": true
}
