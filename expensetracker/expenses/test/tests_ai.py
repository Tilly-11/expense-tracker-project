# expenses/tests/test_ai.py
import numpy as np
import random
from django.test import TestCase
from expenses.ai.sentence_classifier import SimpleCategoryModel

class AITest(TestCase):
    def setUp(self):
        np.random.seed(42)
        random.seed(42)
        self.model = SimpleCategoryModel.load_or_default()

    def test_predict_deterministic(self):
        out1 = self.model.predict(["coffee near me"])
        out2 = self.model.predict(["coffee near me"])
        self.assertEqual(out1, out2)
        cat, conf = out1[0]
        self.assertIsInstance(cat, str)
        self.assertGreaterEqual(conf, 0.0)

    def test_multiple_inputs(self):
        texts = ["buying groceries", "uber ride", "monthly rent"]
        preds = self.model.predict(texts)
        self.assertEqual(len(preds), len(texts))
        for cat, conf in preds:
            self.assertIsInstance(cat, str)
            self.assertGreaterEqual(conf, 0.0)
            self.assertLessEqual(conf, 1.0)

    def test_override_training(self):
        # test that retraining produces a usable model
        model = SimpleCategoryModel()
        model.train(["burger", "bus"], ["Food", "Transport"])
        out = model.predict(["burger"])
        self.assertEqual(out[0][0], "Food")
