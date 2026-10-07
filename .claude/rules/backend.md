# Backend Development Rules

## FastAPI

- Follow FastAPI conventions and idiomatic Python patterns.
- Keep API route handlers thin.
- Route handlers should primarily handle:
  - Request validation
  - Dependency injection
  - Calling business logic
  - Returning responses
- Do not place substantial business logic directly inside route handlers.
- Use FastAPI dependency injection for shared dependencies such as database sessions and authentication.

## Project Structure

Prefer a modular structure such as:

```text
app/
├── main.py
├── config.py
├── models/
├── schemas/
├── routes/
├── services/
├── repositories/
├── dependencies/
├── exceptions/
└── utils/
```

Follow the existing project structure if it differs rather than restructuring the project unnecessarily.

## Pydantic

- Use Pydantic models for request validation and response serialization.
- Keep request schemas separate from database models.
- Use appropriate field types instead of relying on generic strings.
- Use `model_dump()` when converting Pydantic models to dictionaries for internal processing.
- Use `model_validate()` when constructing Pydantic models from ORM/database objects where appropriate.
- Clearly distinguish between create, update, and response schemas.

Example:

```python
class PropertyCreate(BaseModel):
    name: str
    address: str


class PropertyUpdate(BaseModel):
    name: str | None = None
    address: str | None = None


class PropertyResponse(BaseModel):
    id: UUID
    name: str
    address: str
```

## Database Access

- Keep database operations out of route handlers where practical.
- Use repository/service layers when they improve separation of concerns.
- Keep transaction management explicit.
- Do not call `commit()` unnecessarily multiple times within a single logical transaction.
- Use `refresh()` when database-generated values are required after insertion/update.
- Handle rollback appropriately when a transaction fails.

## SQLAlchemy

- Use SQLAlchemy models consistently with the project's database configuration.
- Define relationships and foreign keys explicitly.
- Use appropriate indexes and constraints.
- Avoid N+1 query patterns.
- Avoid loading large datasets unnecessarily.
- Use pagination for potentially large collection endpoints.

## CRUD Operations

For CRUD APIs:

- `POST` → create a resource.
- `GET` → retrieve resources.
- `PUT` → replace/update the resource according to the project's defined semantics.
- `PATCH` → partially update a resource.
- `DELETE` → remove a resource.

Validate resource existence before update/delete operations where appropriate.

Return meaningful HTTP status codes, for example:

- `200 OK` — successful retrieval/update.
- `201 Created` — successful creation.
- `204 No Content` — successful deletion where no response body is required.
- `400 Bad Request` — invalid request.
- `404 Not Found` — resource does not exist.
- `409 Conflict` — resource/state conflict.
- `422 Unprocessable Entity` — request validation failure where appropriate.

## Response Models

- Prefer explicit response models.
- Do not return raw database objects directly from API endpoints.
- Return only fields that API consumers actually need.
- Avoid exposing internal database fields.

## Exception Handling

- Use application-specific exceptions for predictable business errors.
- Use centralized exception handlers for consistent API responses.
- Do not duplicate error formatting across every route.
- Do not return raw Python exception messages to clients.

Example error structure:

```json
{
  "success": false,
  "error": {
    "code": "PROPERTY_NOT_FOUND",
    "message": "Property not found",
    "details": null
  }
}
```

Follow the project's established response format if one already exists.

## Async vs Sync

- Use `async def` only when the underlying operations and dependencies support asynchronous execution.
- Do not use async merely because FastAPI supports it.
- Avoid blocking operations inside async endpoints.

## Logging

- Use the project's logging mechanism instead of `print()`.
- Log useful contextual information.
- Do not log passwords, tokens, API keys, or other sensitive data.

## Documentation

- Use meaningful endpoint summaries and descriptions.
- Keep OpenAPI documentation accurate.
- Document non-obvious business behavior.
- Keep API examples synchronized with actual behavior.