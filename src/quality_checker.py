import cv2
import numpy as np

def check_image_quality(image_path, blur_threshold=100.0, min_area_ratio=0.01):
    image = cv2.imread(image_path)

    if image is None:
        return {
            "is_good": False,
            "message": "Image could not be read.",
            "blur_score": 0,
            "area_ratio": 0,
            "brightness": 0
        }

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = float(np.mean(gray))

    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    signature_pixels = cv2.countNonZero(binary)
    total_pixels = gray.shape[0] * gray.shape[1]
    area_ratio = signature_pixels / total_pixels

    if blur_score < blur_threshold:
        message = "Poor quality: image is blurry. Please re-upload."
        is_good = False
    elif area_ratio < min_area_ratio:
        message = "Poor quality: signature is too small or not visible."
        is_good = False
    elif brightness < 30 or brightness > 245:
        message = "Poor quality: lighting or background is unsuitable."
        is_good = False
    else:
        message = "Good image quality. Ready for verification."
        is_good = True

    return {
        "is_good": is_good,
        "message": message,
        "blur_score": round(float(blur_score), 2),
        "area_ratio": round(float(area_ratio), 4),
        "brightness": round(brightness, 2)
    }
