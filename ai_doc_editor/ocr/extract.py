import pytesseract

def extract_text(path):
    text = pytesseract.image_to_string(path)
    with open("outputs/extracted.txt", "w") as f:
        f.write(text)
