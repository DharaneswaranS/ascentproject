import cv2
import os
from pdf2image import convert_from_path

POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

def preprocess_image(path):
    os.makedirs("processed", exist_ok=True)

    if path.lower().endswith(".pdf"):
        pages = convert_from_path(
            path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )
        img_path = "processed/page_0.png"
        pages[0].save(img_path, "PNG")
    else:
        img_path = path

    img = cv2.imread(img_path)
    if img is None:
        raise ValueError("Image loading failed")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(
        blur, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    output = "processed/clean.png"
    cv2.imwrite(output, thresh)
    return output
