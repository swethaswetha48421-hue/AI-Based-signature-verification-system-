import cv2
import numpy as np

def preprocess_image(image_path, img_size=(128, 128)):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not found or unreadable")
    
    img = cv2.resize(img, img_size)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_normalized = img_gray.astype('float32') / 255.0
    img_final = np.expand_dims(img_normalized, axis=-1)
    img_final = np.expand_dims(img_final, axis=0)
    
    return img_final, img_gray
