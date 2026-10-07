# E-Prop — Property Management REST API

A learning/demo REST API for properties, users and amenities, built with **FastAPI**, **SQLAlchemy 2** and **PostgreSQL**. It uses a layered layout (routes → controllers → services → models) and returns one consistent JSON error format.

> **Status:** The foundation is in place: config, database, models, centralized error handling and tests. The `v1` routes, controllers, services and schemas are still empty packages, so the app only serves `GET /` for now.

---

## Quick start

**Requirements:** Python 3.10+ and a running PostgreSQL instance.

```bash
# 1. Create and activate a virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt        # or: uv pip install -r requirements.txt

# 3. Create the database and configure .env (see below)

# 4. Run
uvicorn app.main:app --reload          # or: uv run uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health/info: `GET /`

On startup the app runs `Base.metadata.create_all`, which creates any missing tables. If PostgreSQL is unreachable, it logs a warning and the server still starts. Don't rely on this for schema changes, because it doesn't alter existing tables. Use migrations for those.

## Configuration

Settings are read from environment variables, or from a `.env` file in the project root, in [app/config/settings.py](app/config/settings.py).

| Variable        | Default                                                          | Purpose                    |
| --------------- | ---------------------------------------------------------------- | -------------------------- |
| `PROJECT_NAME`  | `E-Commerce & Property API`                                      | OpenAPI title              |
| `VERSION`       | `1.0.0`                                                          | OpenAPI version            |
| `API_V1_PREFIX` | `/api/v1`                                                        | Mount path for v1 router   |
| `HOST`, `PORT`  | `127.0.0.1`, `8000`                                              | Bind address               |
| `ENVIRONMENT`   | `development`                                                    | Environment name           |
| `DATABASE_URL`  | `postgresql://admin:your_password@localhost:5432/py_learning_db` | SQLAlchemy connection URL  |

Example `.env`:

```ini
DATABASE_URL="postgresql://admin:<password>@localhost:5432/py_learning_db"
ENVIRONMENT="development"
```

Never commit `.env` or real credentials.

## Project structure

```text
app/
├── main.py            # FastAPI app, logging, lifespan (table creation), router mounting
├── config/            # Settings loaded from env / .env
├── constants/         # error_codes.py, messages.py
├── database/          # Declarative Base, engine, SessionLocal, get_db dependency
├── models/            # SQLAlchemy models: User, Property, Amenities, PropertyAmenities
├── exceptions/        # AppException + centralized handlers (handlers.py)
├── validations/       # Pydantic schemas (error_schema.py; v1/ for request/response schemas)
├── routes/v1/         # Endpoint definitions (inject get_db)
├── controllers/v1/    # Glue between routes and services
├── services/          # Business logic and DB queries
└── utils/             # Shared helpers (e.g. UTC datetime)
tests/                 # pytest suite (in-memory SQLite)
```

A request flows **route → controller → service → model**. [DOCS.md](DOCS.md) walks through each layer line by line.

## Error format

All errors, including validation, HTTP, database and unexpected ones, are returned in one shape by [app/exceptions/handlers.py](app/exceptions/handlers.py):

```json
{
  "success": false,
  "message": "Property not found",
  "code": "PROPERTY_NOT_FOUND",
  "details": null
}
```

- Raise `AppException` (or an `HTTPException`) from services. The handlers map it to this format.
- Validation errors return `422` with `details` as a list of `{field, message, type}`.
- Database errors (`IntegrityError` → `409`, other `SQLAlchemyError` → `500`) are logged server-side. Internals are never exposed to the client.
- Codes and messages live in [app/constants/](app/constants/).

## Testing

```bash
pip install pytest httpx   # not in requirements.txt
pytest
```

Tests use an in-memory SQLite database. [tests/conftest.py](tests/conftest.py) overrides `get_db`, so no PostgreSQL is needed.

## Logging

Logs go to the console and to `app.log` (rotating, 5 MB × 3 backups). `app.log` is a local artifact and shouldn't be committed.

## Contributing

Conventions for contributors (and Claude Code) are in [app/CLAUDE.md](app/CLAUDE.md). The main ones:

- Keep schemas separate from DB models.
- Use the centralized error handling.
- Add or update tests with each behavior change.
- Don't add dependencies without a clear need.
