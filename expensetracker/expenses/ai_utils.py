# expenses/ai.py
import os
from typing import Tuple
from .ai.sentence_classifier import SimpleCategoryModel

_model = None

def _load_model():
    global _model
    if _model is None:
        try:
            _model = SimpleCategoryModel.load_or_default()
        except Exception:
            # Fallback to a default model if loading fails
            _model = SimpleCategoryModel()
            # Train on some basic data
            X = [
                "coffee, cafe", "groceries at supermarket", "monthly rent payment",
                "uber ride", "movie ticket", "restaurant dinner"
            ]
            y = ["Food & Drink", "Groceries", "Rent", "Transport", "Entertainment", "Food & Drink"]
            _model.train(X, y, random_state=42)
    return _model

def predict_category(text: str) -> Tuple[str, float]:
    """
    Returns (predicted_label, confidence_score) using sentence transformer model.
    """
    model = _load_model()
    try:
        predictions = model.predict([text])
        if predictions and len(predictions) > 0:
            return predictions[0]
    except Exception:
        # Fallback rule-based if model prediction fails
        pass
    
    # Fallback rule-based
    txt = text.lower()
    if any(w in txt for w in ['uber', 'bus', 'taxi', 'uber', 'bolt']):
        return 'Transport', 0.6
    if any(w in txt for w in ['restaurant', 'lunch', 'dinner', 'coffee', 'starbucks', 'kfc', 'grocer', 'grocery']):
        return 'Food', 0.6
    if any(w in txt for w in ['electric', 'water', 'bill']):
        return 'Utilities', 0.6
    return 'Other', 0.4
