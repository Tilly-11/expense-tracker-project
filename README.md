# AI-Powered Expense Tracker — README

Short guide to run, test and inspect the API in this repository.

## Project layout (important files)
- Project-level URL conf: [expensetracker/expensetracker/urls.py](expensetracker/expensetracker/urls.py) — API mounted at `/api/`.
- App endpoints: [expenses/urls.py](expenses/urls.py)
- AI model artifacts:
  - [artifacts/model.joblib](artifacts/model.joblib)
  - [expensetracker/models/classifier.joblib](expensetracker/models/classifier.joblib)
- Documentation & guides:
  - [manual_testing_guide.md](manual_testing_guide.md)
  - [API_DOCUMENTATION.md](expensetracker/API_DOCUMENTATION.md)
  - [specifications.md](specifications.md)
  - [requirements.md](requirements.md)

## Prerequisites (Windows)
- Python 3.10+ (or project's supported version)
- Git (optional)
- Recommended virtual environment

## Quick start (Windows PowerShell)
1. Open terminal at project root:
   cd "c:\Users\Shamel\Documents\expense-tracker"

2. Create & activate virtualenv (example):
   - Create: python -m venv .venv
   - Activate (PowerShell): .\.venv\Scripts\Activate.ps1
   - Activate (cmd): .\.venv\Scripts\activate.bat

3. Install dependencies:
   - If `requirements.txt` exists:
     pip install -r requirements.txt
   - If not, follow [requirements.md](requirements.md) to build it and then install.

4. Apply DB migrations:
   - If manage.py is at repo root:
     python manage.py migrate
   - If manage.py is inside `expensetracker/`:
     python expensetracker/manage.py migrate

5. Start dev server:
   python manage.py runserver
   (or python expensetracker/manage.py runserver if needed)

6. Open API docs & schema:
   - Swagger UI: http://127.0.0.1:8000/api/docs/
   - OpenAPI JSON: http://127.0.0.1:8000/api/schema/

   The project routes are mounted under `/api/` — see [expensetracker/expensetracker/urls.py](expensetracker/expensetracker/urls.py) and [expenses/urls.py](expenses/urls.py).

## Manual API checks (examples)
- Get schema:
  curl http://127.0.0.1:8000/api/schema/
- List an endpoint (replace `<endpoint>` with the real path from `expenses/urls.py`):
  curl http://127.0.0.1:8000/api/<endpoint>/
- POST JSON example:
  curl -H "Content-Type: application/json" -X POST -d "{\"amount\":12.5,\"description\":\"test\"}" http://127.0.0.1:8000/api/expenses/

See full step-by-step examples in [manual_testing_guide.md](manual_testing_guide.md).

## Running automated tests
- Using Django test runner:
  python manage.py test
- Using pytest (if configured):
  pip install pytest pytest-django
  pytest

For coverage:
  pip install coverage
  coverage run --source='.' manage.py test
  coverage report -m

Test files live under the `expenses/test` (or `expenses/tests`) directory — consult [implementation_summary.md](implementation_summary.md) for specifics.

## AI models & behavior
- Models used for categorization are saved as joblib artifacts:
  - [artifacts/model.joblib](artifacts/model.joblib)
  - [expensetracker/models/classifier.joblib](expensetracker/models/classifier.joblib)
- AI-related code lives in `expensetracker/expenses/ai` (or `expensetracker/expenses/ai_utils.py`) — see [implementation_plan.md](implementation_plan.md) and [implementation_summary.md](implementation_summary.md) for design notes and how classifiers/anomaly detection are wired into views.
- Ensure `joblib`, `scikit-learn` and `sentence-transformers` (if used) are installed to load/run models.

## Debugging & inspecting routes
- Swagger UI (see above) is the primary reference.
- To print URL patterns locally you can install `django-extensions` and run:
  pip install django-extensions
  Add `'django_extensions'` to INSTALLED_APPS and run:
  python manage.py show_urls

## Notes & troubleshooting
- If tests fail because of missing models, verify the joblib files exist at the paths above.
- If you renamed or moved AI modules, update imports accordingly (implementation notes are in [implementation_summary.md](implementation_summary.md)).
- If `requirements.txt` is missing or incomplete, consult [requirements.md](requirements.md).

## Where to look next
- API behavior and example requests: [API_DOCUMENTATION.md](expensetracker/API_DOCUMENTATION.md)
- Manual walkthrough to validate endpoints: [manual_testing_guide.md](manual_testing_guide.md)
- Project spec and evaluation criteria: [specifications.md](specifications.md)

