import os
import json
import tensorflow as tf
import numpy as np

class SymptomChecker:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '../data/synthetic_symptoms.json')
        self.disclaimer = "DISCLAIMER: This is an AI-powered prediction based on synthetic data. Not a medical diagnosis."

    def predict(self, user_symptoms):
        # Load synthetic data
        try:
            with open(self.data_path, 'r') as f:
                knowledge_base = json.load(f)
        except Exception:
            knowledge_base = []

        # Simple matching logic for demonstration
        best_match = None
        highest_score = 0

        for entry in knowledge_base:
            match_count = len(set(user_symptoms) & set(entry['symptoms']))
            if match_count > highest_score:
                highest_score = match_count
                best_match = entry

        if best_match:
            return {
                "condition": best_match['disease'],
                "confidence": (highest_score / len(best_match['symptoms'])) * 100,
                "advice": best_match['advice'],
                "disclaimer": self.disclaimer
            }

        return {
            "condition": "Unknown condition",
            "confidence": 0,
            "advice": "Please consult a healthcare professional.",
            "disclaimer": self.disclaimer
        }

symptom_checker = SymptomChecker()
