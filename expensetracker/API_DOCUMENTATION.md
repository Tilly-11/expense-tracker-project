# Expense Tracker API Documentation

This document explains how to use the Expense Tracker API in simple terms. This API allows you to manage your expenses, categorize them automatically using AI, and get insights about your spending habits.

## Getting Started

Before using the API, you need to register and get authentication tokens:

### 1. Register a New User

**Endpoint:** `POST /api/auth/register/`

**What it does:** Creates a new user account.

**What you need to send:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**What you get back:**
```json
{
  "id": 1,
  "username": "your_username"
}
```

### 2. Get Authentication Tokens

**Endpoint:** `POST /api/auth/token/`

**What it does:** Gets access and refresh tokens for authentication.

**What you need to send:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**What you get back:**
```json
{
  "refresh": "refresh_token_here",
  "access": "access_token_here"
}
```

Use the `access` token in the `Authorization` header for all other requests:
```
Authorization: Bearer your_access_token_here
```

## Managing Expenses

### 1. Create an Expense

**Endpoint:** `POST /api/expenses/`

**What it does:** Adds a new expense. If you don't specify a category, the AI will predict one for you.

**What you can send:**
```json
{
  "amount": 25.99,
  "description": "Groceries from Walmart",
  "date": "2023-06-15"
}
```

Or with a specific category:
```json
{
  "amount": 25.99,
  "description": "Groceries from Walmart",
  "category": "Food",
  "date": "2023-06-15"
}
```

**What you get back:**
```json
{
  "id": 1,
  "user": 1,
  "amount": "25.99",
  "description": "Groceries from Walmart",
  "category": "Food",
  "predicted_category": "Food",
  "ai_confidence": 0.95,
  "user_override": false,
  "date": "2023-06-15",
  "created_at": "2023-06-15T10:30:00Z",
  "updated_at": "2023-06-15T10:30:00Z"
}
```

### 2. Get All Expenses

**Endpoint:** `GET /api/expenses/`

**What it does:** Lists all your expenses, newest first.

### 3. Get a Specific Expense

**Endpoint:** `GET /api/expenses/{id}/`

**What it does:** Gets details of a specific expense by its ID.

### 4. Update an Expense

**Endpoint:** `PUT /api/expenses/{id}/`

**What it does:** Updates an existing expense.

**What you can send:**
```json
{
  "amount": 29.99,
  "description": "Groceries and cleaning supplies from Walmart",
  "date": "2023-06-15"
}
```

### 5. Override Expense Category

**Endpoint:** `POST /api/expenses/{id}/override/`

**What it does:** Manually sets the category for an expense, overriding the AI prediction.

**What you need to send:**
```json
{
  "category": "Household"
}
```

### 6. Delete an Expense

**Endpoint:** `DELETE /api/expenses/{id}/`

**What it does:** Removes an expense from your records.

## Getting Insights

### Get Spending Insights

**Endpoint:** `GET /api/insights/`

**What it does:** Provides summaries and analysis of your spending.

**What you get back:**
```json
{
  "weekly": [
    {
      "week": "2023-06-11",
      "total": 150.75
    }
  ],
  "monthly": [
    {
      "month": "2023-06-01",
      "total": 520.30
    }
  ],
  "top_categories": [
    {
      "category": "Food",
      "total": 300.50
    }
  ],
  "anomalies": [
    {
      "id": 2,
      "description": "Large purchase at electronics store",
      "amount": 499.99,
      "date": "2023-06-10"
    }
  ]
}
```

This includes:
- Weekly spending summaries for the last 30 days
- Monthly spending summaries for the last 6 months
- Your top 5 spending categories
- Unusual expenses that stand out from your normal spending patterns

## Summary

This API allows you to:
1. Create an account and authenticate
2. Add expenses with automatic category prediction
3. View, update, and delete your expenses
4. Manually override AI predictions
5. Get insights into your spending patterns