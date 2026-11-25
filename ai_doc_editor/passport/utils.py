import fitz  # PyMuPDF

def pdf_to_image(pdf_path):
    doc = fitz.open(pdf_path)
    page = doc[0]

    pix = page.get_pixmap(dpi=300)
    img_path = "outputs/passport_page.png"
    pix.save(img_path)

    return img_path
