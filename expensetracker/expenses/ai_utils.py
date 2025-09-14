# expenses/ai_utils.py
import os
from typing import Tuple, Optional
from django.contrib.auth import get_user_model
from transformers import pipeline
import torch

User = get_user_model()

# Pre-trained zero-shot classification model
_classifier = None
# Minimum confidence threshold for a prediction to be considered certain
CONFIDENCE_THRESHOLD = 0.7

# Default expense categories
DEFAULT_CATEGORIES = [
    "Food & Drink",
    "Groceries",
    "Transport",
    "Entertainment",
    "Utilities",
    "Rent",
    "Healthcare",
    "Shopping",
    "Other"
]

def _load_classifier():
    """Load the pre-trained zero-shot classification model"""
    global _classifier
    if _classifier is None:
        # Use a pre-trained model for zero-shot classification
        # This model can classify text into any categories without retraining
        try:
            _classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1  # Use GPU if available
            )
        except Exception as e:
            print(f"Error loading classifier: {e}")
            # Fallback to CPU if GPU fails
            _classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device=-1
            )
    return _classifier

def get_user_categories(user: User) -> list:
    """
    Get user-specific categories or return default categories.
    In a more advanced implementation, this could retrieve categories
    that the user has previously used or defined.
    """
    if user and user.is_authenticated:
        # For now, we'll use default categories for all users
        # In a more advanced implementation, we could customize this per user
        return DEFAULT_CATEGORIES
    return DEFAULT_CATEGORIES

def predict_category(text: str, user: Optional[User] = None) -> Tuple[str, float]:
    """
    Returns (predicted_label, confidence_score) using a pre-trained zero-shot model.
    If confidence is below threshold, returns ("Uncertain", confidence).
    """
    # Load the classifier
    classifier = _load_classifier()
    
    # Get categories (user-specific or default)
    categories = get_user_categories(user)
    
    try:
        # Perform zero-shot classification
        result = classifier(text, categories)
        
        # Get the top prediction
        if result and 'labels' in result and 'scores' in result:
            label = result['labels'][0]
            confidence = result['scores'][0]
            
            # If confidence is below threshold, mark as uncertain
            if confidence < CONFIDENCE_THRESHOLD:
                return "Uncertain", confidence
            return label, confidence
    except Exception as e:
        print(f"Error in prediction: {e}")
        # Fallback rule-based if model prediction fails
        pass
    
    # Fallback rule-based
    txt = text.lower()
    if any(w in txt for w in ['uber', 'bus', 'taxi', 'bolt']):
        return 'Transport', 0.6
    if any(w in txt for w in ['restaurant', 'lunch', 'dinner', 'coffee', 'starbucks', 'kfc', 'grocer', 'grocery']):
        return 'Food & Drink', 0.6
    if any(w in txt for w in ['electric', 'water', 'bill']):
        return 'Utilities', 0.6
    if any(w in txt for w in ['clothes', 'shoe', 'shopping', 'mall', 'store', 'zara', 'h&m']):
        return 'Shopping', 0.6
    return 'Other', 0.4

def update_user_model_with_feedback(user: User, text: str, category: str):
    """
    With the zero-shot approach, we don't need to update a trained model.
    Instead, we could store the user's preferences or feedback for other purposes.
    For example, we could track which categories a user commonly uses.
    """
    # In this implementation, we don't need to update a model since we're using
    # a pre-trained zero-shot classifier. However, we could store this feedback
    # for analytics or to customize the category list for the user in the future.
    
    if not user.is_authenticated:
        return
        
    # For now, we'll just log that this feedback was provided
    print(f"User {user.id} provided feedback: '{text}' -> '{category}'")
    
    # In a more advanced implementation, you might:
    # 1. Store this feedback in a database for analytics
    # 2. Customize the category list for this user based on their preferences
    # 3. Adjust the confidence threshold based on user feedback
    pass
