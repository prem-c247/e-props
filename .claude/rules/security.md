# Security Rules

## General Security Principles

Follow secure-by-default principles.

- Never trust client-provided input.
- Validate all external input.
- Apply least privilege.
- Fail securely.
- Do not expose internal implementation details.
- Avoid introducing security-sensitive behavior without understanding its implications.

## Secrets

Never hardcode:

- Passwords
- API keys
- JWT secrets
- Database credentials
- Cloud credentials
- Encryption keys
- OAuth client secrets

Use environment variables or an approved secret-management mechanism.

Never commit:

```text
.env
.env.*
credentials.json
*.pem
*.key
```

unless a specific non-sensitive example file is intentionally required.

## Authentication

When authentication is implemented:

- Verify credentials securely.
- Never store plaintext passwords.
- Use a strong password hashing algorithm such as Argon2 or bcrypt.
- Validate authentication tokens properly.
- Apply appropriate token expiration.
- Do not expose authentication secrets in API responses.
- Do not log authentication tokens or passwords.

## Authorization

Authentication and authorization are separate concerns.

Always verify that an authenticated user has permission to perform the requested action.

Do not rely solely on frontend restrictions.

Example:

```text
Authentication:
"Who are you?"

Authorization:
"Are you allowed to perform this action?"
```

## Input Validation

Validate:

- Request bodies
- Query parameters
- Path parameters
- Uploaded files
- External API responses where appropriate

Use Pydantic validation for API input.

Do not rely on frontend validation as the primary security control.

## SQL Injection

- Prefer SQLAlchemy/ORM parameterized queries.
- Never concatenate untrusted input into SQL statements.
- Use raw SQL only when necessary and parameterize all values.

Avoid:

```python
query = f"SELECT * FROM users WHERE id = {user_id}"
```

Prefer parameterized/ORM-based queries.

## API Security

- Use appropriate HTTP status codes.
- Do not expose stack traces.
- Do not return database errors directly to clients.
- Avoid leaking whether sensitive accounts or resources exist when that information should remain private.
- Apply rate limiting to sensitive endpoints where appropriate.
- Use generic responses for operations vulnerable to account enumeration.

## Error Handling

Never expose:

- Stack traces
- File paths
- SQL queries
- Database connection details
- Environment variables
- Internal exception messages
- Credentials or tokens

Client-facing errors should be safe, consistent, and actionable without revealing sensitive implementation details.

## Logging

Never log:

- Passwords
- Access tokens
- Refresh tokens
- API keys
- Authorization headers
- Session secrets
- Sensitive personal information unless explicitly required

Logs should contain enough context to investigate problems without exposing secrets.

## CORS

- Do not use unrestricted CORS in production unless there is a documented reason.
- Avoid:

```python
allow_origins=["*"]
```

for authenticated production APIs.

- Explicitly configure trusted origins where possible.

## File Uploads

If file uploads are implemented:

- Validate file type.
- Validate file size.
- Do not trust the filename or extension.
- Generate safe server-side filenames.
- Store uploads outside executable locations.
- Consider malware scanning for untrusted files.
- Prevent path traversal.

## Dependency Security

- Keep dependencies reasonably up to date.
- Review security advisories for important dependencies.
- Avoid adding packages with unknown or unnecessary security implications.
- Do not disable security tooling merely to make builds pass without understanding the reason.

## Sensitive Data

Treat the following as sensitive:

- Passwords
- Authentication tokens
- Financial information
- Personal information
- Private user data
- Security credentials

Only collect, store, process, and return data that is necessary for the application's purpose.

## Security Changes

Before implementing security-sensitive changes:

1. Understand the existing authentication and authorization flow.
2. Check how errors and logging currently work.
3. Check whether the change affects existing clients.
4. Prefer centralized security controls over duplicated checks.
5. Test both authorized and unauthorized scenarios.

Never weaken an existing security control just to make an implementation easier.