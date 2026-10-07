# E-Prop Project — Claude Code Instructions

## Project Overview

E-Prop is a learning/demo property management REST API built with Python and FastAPI.

The project is intended to follow production-oriented software engineering practices while remaining simple enough for learning and experimentation.

## General Principles

- Prefer simple, readable, maintainable solutions over unnecessary complexity.
- Follow existing project structure and conventions before introducing new patterns.
- Reuse existing utilities, services, schemas, and helpers where appropriate.
- Do not introduce new dependencies unless they are necessary and justified.
- Keep changes focused on the requested task.
- Do not modify unrelated files or functionality.
- Preserve backward compatibility unless the task explicitly requires a breaking change.
- Follow Python and FastAPI best practices.
- Use clear and descriptive names for variables, functions, classes, modules, and API endpoints.
- Add comments only when they explain non-obvious behavior or design decisions.

## Code Quality

- Write clean, modular, and readable code.
- Avoid duplicated logic.
- Keep functions and classes focused on a single responsibility.
- Prefer explicit code over clever or overly compact implementations.
- Use type hints consistently.
- Handle expected errors explicitly.
- Avoid silently swallowing exceptions.
- Do not leave debugging statements such as `print()` in production code.

## API Development

- Follow RESTful API conventions.
- Use appropriate HTTP methods and status codes.
- Validate request data using Pydantic schemas.
- Keep request/response schemas separate from database models.
- Use consistent API response and error formats.
- Do not expose internal implementation details or sensitive information in API responses.

## Database

- Keep database access separate from API route handlers.
- Use the project's configured ORM/database layer.
- Do not construct raw SQL unless there is a clear requirement.
- Use migrations for schema changes.
- Do not modify or delete production data as part of development tasks.
- Consider relationships, constraints, indexes, and data integrity when changing models.

## Error Handling

- Use centralized exception handling where possible.
- Return consistent error responses.
- Do not expose stack traces, database errors, or internal implementation details to API consumers.
- Log useful diagnostic information on the server side when appropriate.

## Testing

- Add or update tests when behavior changes.
- Test successful scenarios as well as expected failure scenarios.
- Do not remove existing tests simply to make a change pass.
- Run relevant tests after making changes.

## Dependencies

Before adding a package:

1. Check whether the functionality already exists in the project.
2. Prefer the Python standard library when appropriate.
3. Prefer existing project dependencies when possible.
4. Add a dependency only when it provides clear value.

## Git

- Keep changes small and focused.
- Do not modify Git history unless explicitly requested.
- Do not commit secrets, credentials, `.env` files, generated files, or local development artifacts.
- Do not create commits unless explicitly requested.

## Environment Configuration

- Never hardcode credentials, API keys, passwords, tokens, or secrets.
- Use environment variables/configuration for environment-specific values.
- Do not modify `.env` files unless explicitly requested.
- Preserve the separation between development, testing, and production configuration.

## Claude Code Behavior

Before making changes:

1. Understand the existing implementation.
2. Identify the files affected by the requested change.
3. Follow existing project conventions.
4. Make the smallest appropriate change.

After making changes:

1. Review the modified code.
2. Check for obvious regressions.
3. Run relevant tests or validation commands when available.
4. Summarize what was changed and why.
5. Mention any assumptions or remaining concerns.

Do not make unrelated refactoring unless explicitly requested.