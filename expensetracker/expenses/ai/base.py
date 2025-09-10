from abc import ABC, abstractmethod

class BaseCategoryModel(ABC):
    @abstractmethod
    def predict(self, texts: list):
        """Return list of (category, confidence) for each text"""
        pass

    @abstractmethod
    def train(self, X_texts: list, y_labels: list, random_state:int=42):
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @classmethod
    @abstractmethod
    def load(cls, path: str):
        pass