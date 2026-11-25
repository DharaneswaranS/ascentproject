import pytesseract

def validate_document(path):
    data = pytesseract.image_to_data(path, output_type=pytesseract.Output.DICT)
    confidences = [int(c) for c in data["conf"] if c != "-1"]

    avg_conf = sum(confidences) / len(confidences)

    if avg_conf < 60:
        return False, avg_conf

    return True, avg_conf
