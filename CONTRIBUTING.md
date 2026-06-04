# Contributing

## Development Setup

### Prerequisites
- Python 3.11+ (tested on 3.11 and 3.12)
- pip or poetry

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Running Tests

Run the test suite locally:

```bash
python -m pytest -q
```

Run tests with coverage reporting:

```bash
python -m pytest --cov=src --cov-report=term-missing
```

## Starting the App

### Option 1: Development Server (with auto-reload)

```bash
cd src
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The app will be available at **http://localhost:8000**

### Option 2: Production Server (single process)

```bash
cd src
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` — Redirects to the static index page
- `GET /activities` — Returns all available activities
- `POST /activities/{activity_name}/signup` — Sign up a student for an activity

### Signup Example

```bash
curl -X POST http://localhost:8000/activities/Chess%20Club/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "student@mergington.edu"}'
```

## Code Style

- Follow PEP 8 for Python code
- Keep functions small and focused
- Add docstrings to new endpoints

## Running CI Locally

To simulate the GitHub Actions workflow:

```bash
# Test on Python 3.11 and 3.12
python3.11 -m pytest --cov=src --cov-report=term-missing
python3.12 -m pytest --cov=src --cov-report=term-missing
```

## Questions?

Open an issue or check the [README.md](README.md) for more details.
