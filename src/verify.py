from tensorflow.keras.models import load_model
from src.preprocess import preprocess_image

def verify_signature(image_path, model_path='models/signature_cnn_model.h5'):
    model = load_model(model_path)
    img_array, img_gray = preprocess_image(image_path)
    
    prediction = model.predict(img_array)[0][0]
    confidence = float(prediction)
    
    if confidence > 0.5:
        result = "Genuine"
        confidence_percent = confidence * 100
    else:
        result = "Forged"
        confidence_percent = (1 - confidence) * 100
    
    return {
        'result': result,
        'confidence': confidence_percent,
        'raw_score': confidence
    }
