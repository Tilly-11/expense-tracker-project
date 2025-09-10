import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from joblib import dump, load

from .base import BaseCategoryModel

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
EMBED_MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'  # lightweight
EMBED_DIM = 384  # for that model

class SimpleCategoryModel(BaseCategoryModel):
    def __init__(self, embedder=None, clf=None, label_encoder=None):
        self.embedder = embedder or SentenceTransformer(EMBED_MODEL_NAME)
        self.clf = clf
        self.le = label_encoder

    def predict(self, texts):
        X = self.embedder.encode(texts, convert_to_numpy=True)
        probs = self.clf.predict_proba(X)
        preds_idx = probs.argmax(axis=1)
        preds = self.le.inverse_transform(preds_idx)
        confidences = probs.max(axis=1)
        return list(zip(preds.tolist(), confidences.tolist()))

    def train(self, X_texts, y_labels, random_state=42):
        np.random.seed(random_state)
        self.le = LabelEncoder()
        y = self.le.fit_transform(y_labels)
        X = self.embedder.encode(X_texts, convert_to_numpy=True)
        clf = LogisticRegression(max_iter=1000, random_state=random_state)
        clf.fit(X, y)
        self.clf = clf

    def save(self, path=None):
        if path is None:
            path = os.path.join(MODEL_DIR, 'classifier.joblib')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        dump({
            'clf': self.clf,
            'label_encoder': self.le
        }, path)
        # embedder uses huggingface cache; optionally save model dir

    @classmethod
    def load(cls, path=None):
        if path is None:
            path = os.path.join(MODEL_DIR, 'classifier.joblib')
        obj = load(path)
        model = cls()
        model.clf = obj['clf']
        model.le = obj['label_encoder']
        return model

    @classmethod
    def load_or_default(cls):
        path = os.path.join(MODEL_DIR, 'classifier.joblib')
        if os.path.exists(path):
            return cls.load(path)
        # If no saved model, return a default trivial model trained on tiny synthetic data
        model = cls()
        # tiny deterministic training data:
        X = [
            "coffee, cafe", "groceries at supermarket", "monthly rent payment",
            "uber ride", "movie ticket", "restaurant dinner"
        ]
        y = ["Food & Drink", "Groceries", "Rent", "Transport", "Entertainment", "Food & Drink"]
        model.train(X, y, random_state=42)
        model.save(path)
        return model