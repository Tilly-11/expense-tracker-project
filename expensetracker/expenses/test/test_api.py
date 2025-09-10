# expenses/tests/test_api.py
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework import status
import os
import joblib

User = get_user_model()

class ExpenseAPITests(APITestCase):
    def setUp(self):
        # deterministic seed for numpy/sklearn if used in tests
        import numpy as np, random
        np.random.seed(42)
        random.seed(42)

        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')  # optional
        # Or use JWT token obtain to authenticate
        resp = self.client.post(reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'password123'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        token = resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_create_expense_without_category_triggers_ai(self):
        url = reverse('expenses-list')
        payload = {
            'amount': '12.50',
            'description': 'Lunch at subway',
            'date': '2025-09-01'
        }
        r = self.client.post(url, payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        # predicted_category should be present
        self.assertIn('predicted_category', r.data)
        self.assertIn('ai_confidence', r.data)

    def test_override_category(self):
        url = reverse('expenses-list')
        payload = {
            'amount': '50.00',
            'description': 'Taxi to airport',
            'date': '2025-09-02'
        }
        r = self.client.post(url, payload, format='json')
        pk = r.data['id']
        override_url = reverse('expenses-override', args=[pk])
        r2 = self.client.post(override_url, {'category': 'Transport'}, format='json')
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        self.assertEqual(r2.data['category'], 'Transport')
        self.assertTrue(r2.data['user_override'])
