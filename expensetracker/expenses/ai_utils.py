# expenses/ai.py
import os
from typing import Tuple, Optional
from django.contrib.auth import get_user_model
from expenses.ai.sentence_classifier import SimpleCategoryModel
from expenses.ai.user_model import UserCategoryModel

User = get_user_model()

# Global fallback model (the original shared model)
_global_model = None
# Minimum confidence threshold for a prediction to be considered certain
CONFIDENCE_THRESHOLD = 0.7

def _load_global_model():
    """Load the global fallback model"""
    global _global_model
    if _global_model is None:
        try:
            _global_model = SimpleCategoryModel.load_or_default()
        except Exception:
            # Fallback to a default model if loading fails
            _global_model = SimpleCategoryModel()
            # Enhanced training data with more categories and examples
            X = [
                # Shopping
                "bought new shoes", "clothes shopping", "new t-shirt", "jeans from h&m",
                "nike sneakers", "shopping mall purchases", "accessories from zara",
                
                # Food & Drink
                "coffee at starbucks", "lunch at restaurant", "groceries shopping",
                "dinner with friends", "takeout food", "cafe breakfast",
                
                # Transport
                "uber ride home", "taxi to work", "bus ticket", "train pass",
                "monthly metro card", "bolt ride airport",
                
                # Entertainment
                "movie tickets", "concert tickets", "netflix subscription",
                "theater show", "museum entry", "theme park",
                
                # Utilities
                "electricity bill", "water bill", "internet payment",
                "phone bill", "gas bill", "utility payment",
                
                # Rent
                "monthly rent", "apartment payment", "housing rent",
                
                # Healthcare
                "doctor visit", "medicine", "pharmacy purchase",
                "medical checkup", "dental cleaning"
            ]
            
            y = [
                # Shopping categories
                "Shopping", "Shopping", "Shopping", "Shopping",
                "Shopping", "Shopping", "Shopping",
                
                # Food categories
                "Food & Drink", "Food & Drink", "Groceries",
                "Food & Drink", "Food & Drink", "Food & Drink",
                
                # Transport categories
                "Transport", "Transport", "Transport", "Transport",
                "Transport", "Transport",
                
                # Entertainment categories
                "Entertainment", "Entertainment", "Entertainment",
                "Entertainment", "Entertainment", "Entertainment",
                
                # Utilities categories
                "Utilities", "Utilities", "Utilities",
                "Utilities", "Utilities", "Utilities",
                
                # Rent categories
                "Rent", "Rent", "Rent",
                
                # Healthcare categories
                "Healthcare", "Healthcare", "Healthcare",
                "Healthcare", "Healthcare"
            ]
            
            _global_model.train(X, y, random_state=42)
    return _global_model

def get_user_model(user: User) -> UserCategoryModel:
    """
    Load or create a user-specific model.
    """
    if user.is_authenticated:
        return UserCategoryModel.load_or_default(user.id)
    return None

def predict_category(text: str, user: Optional[User] = None) -> Tuple[str, float]:
    """
    Returns (predicted_label, confidence_score) using user-specific or global model.
    If confidence is below threshold, returns ("Uncertain", confidence).
    """
    model_to_use = _global_model
    
    # Try to use user-specific model if user is provided
    if user and user.is_authenticated:
        user_model = get_user_model(user)
        if user_model and user_model.is_trained():
            model_to_use = user_model
        else:
            # If user model isn't trained, fall back to global model
            model_to_use = _load_global_model()
    else:
        # If no user or not authenticated, use global model
        model_to_use = _load_global_model()
    
    try:
        predictions = model_to_use.predict([text])
        if predictions and len(predictions) > 0:
            label, confidence = predictions[0]
            # If confidence is below threshold, mark as uncertain
            if confidence < CONFIDENCE_THRESHOLD:
                return "Uncertain", confidence
            return label, confidence
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
    if any(w in txt for w in ['clothes', 'shoe', 'shopping', 'mall', 'store', 'zara', 'h&m']):
        return 'Shopping', 0.6
    return 'Other', 0.4

def update_user_model_with_feedback(user: User, text: str, category: str):
    """
    Update the user's model with a new training example.
    """
    if not user.is_authenticated:
        return
        
    user_model = get_user_model(user)
    if not user_model:
        user_model = UserCategoryModel(user_id=user.id)
    
    # For simplicity, we'll do a full retrain with the new data
    # In a production environment, you might want to collect examples
    # and do batch updates or use partial_fit more effectively
    try:
        # Get existing training data for this user from the database
        # This is a simplified approach - in reality, you might want to store
        # training examples in a separate table or cache
        from expenses.models import Expense
        user_expenses = Expense.objects.filter(user=user, user_override=True).exclude(category__isnull=True).exclude(category__exact='')
        
        X_texts = [e.description for e in user_expenses]
        y_labels = [e.category for e in user_expenses]
        
        # Add the new example
        X_texts.append(text)
        y_labels.append(category)
        
        # Retrain the model
        if len(X_texts) > 0:
            user_model.train(X_texts, y_labels)
            user_model.save()
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error updating user model for user {user.id}: {e}")
