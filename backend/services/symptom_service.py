import tensorflow as tf
import numpy as np

class SymptomChecker:
    def __init__(self):
        # In a real app, load a pre-trained model:
        # self.model = tf.keras.models.load_model('models/symptom_model.h5')
        self.diseases = ["Common Cold", "Flu", "Allergy", "Gastroenteritis", "Migraine"]

    def predict(self, symptoms_list):
        # Mock prediction logic for hackathon demonstration
        # In production, this would use the TF model to return probabilities
        confidence = np.random.uniform(0.7, 0.95)
        suggestion = np.random.choice(self.diseases)
        
        return {
            "prediction": suggestion,
            "confidence": round(confidence, 2),
            "disclaimer": "This is an AI prediction. Please consult a healthcare professional for accurate diagnosis."
        }

symptom_checker = SymptomChecker()
