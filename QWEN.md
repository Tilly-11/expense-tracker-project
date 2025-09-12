# Qwen Code Context for Expense Tracker Project

## Project Overview

This is a Django-based REST API for an AI-powered expense tracker. The application allows users to manage their expenses, with the added functionality of AI-driven expense categorization and spending insights.

### Key Technologies

- **Framework**: Django (v5.2.6) with Django REST Framework
- **Authentication**: JWT (via `djangorestframework-simplejwt`)
- **API Documentation**: Swagger/OpenAPI 3.0 (via `drf-spectacular`)
- **AI/ML**: Scikit-learn, Joblib, Sentence Transformers
- **Database**: SQLite (default, as indicated by `db.sqlite3`)

### Core Components

1. **Expense Management**: Standard CRUD operations for user expenses.
2. **AI Categorization**: Automatic prediction of expense categories based on description using a sentence transformer model.
3. **User Override**: Ability for users to manually set/override AI predictions.
4. **Spending Insights**: API endpoints providing weekly/monthly summaries, top categories, and anomaly detection.
5. **Authentication**: User registration and JWT-based authentication.

### Project Structure (Key Files)

- `README.md`: Instructions for setup, running, and testing the API.
- `specifications.md`: Detailed requirements for the backend engineering assessment.
- `expensetracker/requirements.txt`: Python dependencies.
- `expensetracker/expenses/models.py`: Defines the `Expense` model, including fields for user input (`category`) and AI output (`predicted_category`, `ai_confidence`).
- `expensetracker/expenses/ai_utils.py`: Core logic for loading the AI model and predicting expense categories.
- `expensetracker/expenses/views.py`: Django REST Framework views, including `ExpenseViewSet` and `InsightsAPIView`.
- `expensetracker/expenses/serializers.py`: Serializers for the `Expense` model, integrating AI prediction during creation.
- `expensetracker/expenses/urls.py`: API routes for expenses, insights, and authentication.
- `expensetracker/API_DOCUMENTATION.md`: User-friendly documentation for the API endpoints.
- `artifacts/model.joblib`: Serialized AI model file.

## Building and Running

### Prerequisites

- Python 3.10+
- Git (optional)
- Virtual environment tool (e.g., `venv`)

### Setup Instructions (Windows - PowerShell)

1. **Navigate to the project root** (where `README.md` is located).
2. **Create and activate a virtual environment**:

    ```bash
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```

3. **Install dependencies**:

    ```bash
    pip install -r expensetracker/requirements.txt
    ```

4. **Apply database migrations**:

    ```bash
    python expensetracker/manage.py migrate
    ```

5. **(Optional) Create a superuser for admin access**:

    ```bash
    python expensetracker/manage.py createsuperuser
    ```

### Running the Development Server

- From the project root:

    ```bash
    python expensetracker/manage.py runserver
    ```

- The API will be available at `http://127.0.0.1:8000/`.
- Swagger UI documentation: `http://127.0.0.1:8000/api/docs/`
- OpenAPI JSON schema: `http://127.0.0.1:8000/api/schema/`

## Development Conventions

- **RESTful Design**: API endpoints follow REST principles.
- **DRF ViewSets**: `ExpenseViewSet` is used for standard CRUD operations on expenses.
- **Custom Actions**: AI override is implemented as a custom action `override` on the `ExpenseViewSet`.
- **AI Integration**: AI prediction logic is encapsulated in `ai_utils.py` and called during expense creation if no category is provided.
- **API Documentation**: Endpoints are documented using `drf-spectacular` decorators (`@extend_schema`).
- **Authentication**: Required for expense and insights endpoints using JWT.
- **Testing**: Tests should be written using Django's test runner or pytest, ensuring AI-related tests are deterministic (e.g., by setting random seeds or mocking models).

## Key API Endpoints

- `POST /api/auth/register/`: Register a new user.
- `POST /api/auth/token/`: Obtain JWT tokens.
- `GET /api/expenses/`: List all user's expenses.
- `POST /api/expenses/`: Create a new expense (AI prediction triggered if category omitted).
- `POST /api/expenses/{id}/override/`: Manually override the category of an expense.
- `GET /api/insights/`: Get spending summaries and anomalies.

## AI Model Notes

- The AI model is a sentence transformer classifier, saved as `artifacts/model.joblib`.
- The `ai_utils.py` file handles loading this model and making predictions.
- If the model file is missing or incompatible, the system falls back to a simple rule-based categorization.
- Ensure `joblib` and `scikit-learn` are installed to load the model correctly.
