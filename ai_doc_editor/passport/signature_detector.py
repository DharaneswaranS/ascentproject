import cv2

def detect_signature(image_path):
    img = cv2.imread(image_path, 0)
    h, w = img.shape

    roi = img[int(h * 0.6):h, 0:w]
    _, thresh = cv2.threshold(roi, 150, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    signature_like = [
        c for c in contours if cv2.contourArea(c) > 700
    ]

    return len(signature_like) > 0
