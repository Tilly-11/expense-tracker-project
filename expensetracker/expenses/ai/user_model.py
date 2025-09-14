import os
from django.contrib.auth import get_user_model
from .base import BaseCategoryModel

User = get_user_model()

class UserCategoryModel(BaseCategoryModel):
    """
    Updated implementation that works with the pre-trained zero-shot model approach.
    This class is kept for compatibility but doesn't train or use a separate model.
    """
    def __init__(self, user_id=None):
        self.user_id = user_id
        # No model initialization needed for the zero-shot approach
        
    def _get_model_path(self):
        """
        With the new approach, we don't save user-specific models.
        This method is kept for compatibility but will not be used.
        """
        return None
        
    def is_trained(self):
        """
        With the new approach, we don't have a trained model.
        This method is kept for compatibility but returns False.
        """
        return False
        
    def predict(self, texts):
        """
        With the new approach, we don't use this class for prediction.
        Predictions are handled directly in ai_utils.py with the zero-shot model.
        This method is kept for compatibility but will not be used.
        """
        # Return uncertain predictions as fallback
        return [("Uncertain", 0.1)] * len(texts)

    def train(self, X_texts, y_labels, random_state=42):
        """
        With the new approach, we don't need to train user-specific models.
        This method is kept for compatibility but does nothing.
        """
        pass

    def partial_fit(self, X_texts, y_labels):
        """
        With the new approach, we don't need to incrementally update models.
        This method is kept for compatibility but does nothing.
        """
        pass
        
    def save(self, path=None):
        """
        With the new approach, we don't need to save user-specific models.
        This method is kept for compatibility but does nothing.
        """
        pass

    @classmethod
    def load(cls, path):
        """
        With the new approach, we don't load user-specific models.
        This method is kept for compatibility but returns None.
        """
        return None

    @classmethod
    def load_or_default(cls, user_id):
        """
        With the new approach, we don't need user-specific models.
        This method is kept for compatibility but returns a default instance.
        """
        return cls(user_id=user_id)