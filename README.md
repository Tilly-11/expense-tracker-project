# AI-Powered Expense Tracker — README

Short, focused instructions to run, test and inspect the API in this repository.

Important files
- Project URLs: [expensetracker/expensetracker/urls.py](expensetracker/expensetracker/urls.py) (API mounted at /api/)
- App routes: [expensetracker/expenses/urls.py](expensetracker/expenses/urls.py)
- Model artifact: [artifacts/model.joblib](artifacts/model.joblib)
- Project spec: [specifications.md](specifications.md)

Prerequisites (Windows)
- Python 3.10+ (or the version your environment uses)
- Git (optional)
- Recommended: create an isolated virtual environment

Quick start (PowerShell)
1. Open terminal at project root

2. Create and activate a virtual environment:
   - Create: python -m venv .venv
   - Activate (PowerShell): .\.venv\Scripts\Activate.ps1
   - Activate (cmd): .\.venv\Scripts\activate.bat

3. Install dependencies:
   ```
   pip install -r expensetracker/requirements.txt
   ```

4. Apply database migrations:
   ```
   python expensetracker/manage.py migrate
   ```

5. Create a superuser (optional, for admin UI):
   ```
   python expensetracker/manage.py createsuperuser
   ```

Run the development server
```
python expensetracker/manage.py runserver
```

API docs and schema (provided by drf-spectacular)
- Swagger UI: http://127.0.0.1:8000/api/docs/
- OpenAPI JSON: http://127.0.0.1:8000/api/schema/

Quick manual API checks (replace `<endpoint>` with real paths from [expensetracker/expenses/urls.py](expensetracker/expenses/urls.py))
- Get OpenAPI schema:
  ```
  curl http://127.0.0.1:8000/api/schema/
  ```
- List endpoint:
  ```
  curl http://127.0.0.1:8000/api/<endpoint>/
  ```
- Create (example):
  ```
  curl -H "Content-Type: application/json" -X POST -d "{\"amount\":12.5,\"description\":\"test\"}" http://127.0.0.1:8000/api/expenses/
  ```

AI model notes
- Classification model artifact: [artifacts/model.joblib](artifacts/model.joblib). Ensure `joblib` and `scikit-learn` are installed to load this file.
- The system now supports user-specific AI models that learn from your expense categorization patterns.
- If the model file is missing or incompatible the AI endpoints may return errors — check log output for file-not-found or deserialization errors.
- The AI will indicate when it's uncertain about a prediction (confidence < 70%), allowing for better user interaction.

Running tests
```
python expensetracker/manage.py test
```

- If using pytest:
  ```
  pip install pytest pytest-django
  pytest
  ```
- For deterministic AI-related tests, ensure tests set fixed random seeds and that model artifacts exist or are mocked.

Troubleshooting
- If endpoints 500, check server logs in the terminal for missing imports, missing model files, or migration issues.
- To list URL patterns (install django-extensions):
  ```
  pip install django-extensions
  ```
  Add 'django_extensions' to INSTALLED_APPS, then:
  ```
  python expensetracker/manage.py show_urls
  ```

Where to look next
- Inspect app routes: open [expensetracker/expenses/urls.py](expensetracker/expenses/urls.py)
- Inspect project routing and API mounting: [expensetracker/expensetracker/urls.py](expensetracker/expensetracker/urls.py)
- Model artifact and sample phrases: [artifacts/model.joblib](artifacts/model.joblib)
