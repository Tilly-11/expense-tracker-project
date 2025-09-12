import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load
from django.contrib.auth import get_user_model

from expenses.ai.base import BaseCategoryModel

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
EMBED_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'  # lightweight
MIN_TRAINING_SAMPLES = 10  # Minimum samples needed to train a decent model

User = get_user_model()

class UserCategoryModel(BaseCategoryModel):
    def __init__(self, user_id=None, embedder=None, clf=None, label_encoder=None):
        self.user_id = user_id
        self.embedder = embedder or SentenceTransformer(EMBED_MODEL_NAME)
        self.clf = clf
        self.le = label_encoder
        # For SGDClassifier, we need to keep track of seen classes for partial_fit
        self._classes = np.array([]) if clf is None else getattr(clf, 'classes_', np.array([]))
        
    def _get_model_path(self):
        if self.user_id is None:
            raise ValueError("User ID is required to get model path for UserCategoryModel")
        return os.path.join(MODEL_DIR, f'user_{self.user_id}', 'classifier.joblib')
        
    def is_trained(self):
        """Check if the model has been trained with sufficient data"""
        return self.clf is not None and len(self._classes) >= 2 and hasattr(self.clf, 'coef_')
        
    def predict(self, texts):
        if not self.is_trained():
            # If not trained, return low confidence for all
            return [("Uncertain", 0.1)] * len(texts)
            
        X = self.embedder.encode(texts, convert_to_numpy=True)
        try:
            probs = self.clf.predict_proba(X)
            preds_idx = probs.argmax(axis=1)
            preds = self.le.inverse_transform(preds_idx)
            confidences = probs.max(axis=1)
            return list(zip(preds.tolist(), confidences.tolist()))
        except Exception:
            # If prediction fails (e.g., new text with no clear class), return uncertain
            return [("Uncertain", 0.1)] * len(texts)

    def train(self, X_texts, y_labels, random_state=42):
        """Initial training of the model"""
        if len(X_texts) < MIN_TRAINING_SAMPLES:
            # Not enough data to train a reliable model
            self.clf = None
            self.le = None
            self._classes = np.array([])
            return
            
        np.random.seed(random_state)
        self.le = LabelEncoder()
        y = self.le.fit_transform(y_labels)
        self._classes = np.unique(y)
        X = self.embedder.encode(X_texts, convert_to_numpy=True)
        
        # Use SGDClassifier for online learning capability
        clf = SGDClassifier(random_state=random_state, learning_rate='constant', eta0=0.01)
        clf.fit(X, y)
        self.clf = clf

    def partial_fit(self, X_texts, y_labels):
        """Incrementally update the model with new data"""
        if len(X_texts) == 0:
            return
            
        # If model is not initialized, do initial training
        if not self.is_trained():
            self.train(X_texts, y_labels)
            return
            
        # Encode new data
        y_new = self.le.transform(y_labels)  # Assuming labels are already known to the encoder
        # If there are new labels, we might need to handle them (for simplicity, we'll skip for now)
        # A more robust implementation would refit the label encoder or use a different approach
        new_classes = np.unique(y_new)
        all_classes = np.unique(np.concatenate([self._classes, new_classes]))
        
        if not np.array_equal(all_classes, self._classes):
            # New classes detected, need to handle this case
            # For simplicity, we'll refit the model with combined data
            # In a production system, you might want a more sophisticated approach
            # like resetting the model or using a classifier that handles new classes better
            # For now, we'll just skip partial fit if new classes are detected
            # and rely on full retraining when needed
            return
            
        X_new = self.embedder.encode(X_texts, convert_to_numpy=True)
        self.clf.partial_fit(X_new, y_new)
        
    def save(self, path=None):
        if path is None:
            path = self._get_model_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        dump({
            'clf': self.clf,
            'label_encoder': self.le,
            'classes': self._classes,
            'user_id': self.user_id
        }, path)
        # embedder uses huggingface cache; optionally save model dir

    @classmethod
    def load(cls, path):
        if not os.path.exists(path):
            return None
        try:
            obj = load(path)
            model = cls(user_id=obj.get('user_id'))
            model.clf = obj['clf']
            model.le = obj['label_encoder']
            model._classes = obj.get('classes', np.array([]))
            return model
        except Exception:
            # If loading fails, return None to trigger fallback
            return None

    @classmethod
    def load_or_default(cls, user_id):
        """Load user-specific model or return a default untrained model"""
        model = cls(user_id=user_id)
        path = model._get_model_path()
        loaded_model = cls.load(path)
        if loaded_model:
            return loaded_model
        return model