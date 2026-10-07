# FastAPI Architecture & Line-by-Line Beginner Guide

Welcome to the comprehensive, line-by-line architectural guide!
Because you are coming from **Node.js** and **PHP**, this guide connects every single Python & FastAPI concept to things you already know (`express.Router`, controllers, services, Zod/Joi, Eloquent).

---

## 1. The Big Picture: How a Request Travels

When a client sends `POST http://localhost:8000/properties/` with JSON data, the request flows through these layers in exact order:

```
1. Client sends HTTP Request
   │
   ▼
2. app/main.py                     (Loads FastAPI, mounts routers)
   │
   ▼
3. app/routes/v1/__init__.py       (Master router; forwards /properties to property router)
   │
   ▼
4. app/routes/v1/property_routes.py (Matches HTTP Method & URL; triggers Pydantic validation)
   │
   ▼
5. app/controllers/v1/property_controller.py (Handles HTTP logic; throws 404/400 if needed)
   │
   ▼
6. app/services/v1/property_service.py (Business logic: generates UUID, timestamps, prepares object)
   │
   ▼
7. app/services/store.py           (Saves to in-memory database table: properties_db)
   │
   ▼
8. Response travels back up to the client as clean JSON!
```

---

## 2. Layer 1: Validations / Schemas (`validations/v1/property_schema.py`)

In Node.js, you might use **Zod** or **Joi**. In PHP, you use **FormRequest** or **typed DTOs**.
In Python, we use **Pydantic**. Pydantic models define what data is allowed into the API, and what data gets sent back out.

### Code Sample:
```python
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class PropertyBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    area: float

class PropertyCreate(PropertyBase):
    pass

class PropertyResponse(PropertyBase):
    id: UUID
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### Line-by-Line Explanation:
- `class PropertyBase(BaseModel):`
  - Inheriting from `BaseModel` gives this class superpowers: automatic validation, type coercion, and JSON conversion.
- `title: str`:
  - Required field. If the user sends a number or omits `title`, FastAPI rejects it immediately with a `422 Unprocessable Entity` error before touching your controller!
- `description: Optional[str] = None`:
  - Optional field. Defaults to `None` (Python's `null`).
- `price: float`, `area: float`:
  - Numbers with decimals. If the client sends `"450000"` as a string, Pydantic converts it to a float automatically.
- `class PropertyCreate(PropertyBase): pass`:
  - What the client sends on `POST /properties`. It inherits all fields from `PropertyBase`.
- `class PropertyResponse(PropertyBase):`:
  - What the server sends back to the client. It has everything in `PropertyBase`, plus `id` and `created_at`.
- `model_config = ConfigDict(from_attributes=True)`:
  - In Pydantic v2, this allows the schema to read data from dictionary keys or Python object attributes interchangeably (crucial when we switch to SQLAlchemy models later!).

---

## 3. Layer 2: Routes (`routes/v1/property_routes.py`)

In Node.js, this is `router.post('/', ...)` in Express. In Laravel, this is `Route::post('/', ...)`.
Routes define **URL paths** and **HTTP methods** (`GET`, `POST`, `PUT`, `DELETE`).

### Code Sample:
```python
from fastapi import APIRouter, status
from app.controllers.v1 import property_controller
from app.validations.v1.property_schema import PropertyCreate, PropertyResponse

router = APIRouter()

@router.post("/", response_model=PropertyResponse, status_code=status.HTTP_201_CREATED)
def create_property(payload: PropertyCreate):
    return property_controller.create_property(payload)
```

### Line-by-Line Explanation:
- `router = APIRouter()`:
  - Creates a mini-router instance, identical to `const router = express.Router()` in Express.
- `@router.post(...)`:
  - A Python **decorator** (starts with `@`). It tells FastAPI: *"When an HTTP POST hits `/`, execute the function directly below this line"*.
- `response_model=PropertyResponse`:
  - Filters and shapes the outgoing response. Even if your internal data has extra secret fields, FastAPI only serializes what is defined in `PropertyResponse`.
- `status_code=status.HTTP_201_CREATED`:
  - Automatically sets the HTTP response status to `201 Created` (instead of the default `200 OK`).
- `def create_property(payload: PropertyCreate):`:
  - `payload: PropertyCreate` tells FastAPI: *"Read the incoming JSON body, validate it against `PropertyCreate`, and pass it to this parameter"*.
- `return property_controller.create_property(payload)`:
  - Routes stay lean. They do NOT write business logic; they immediately delegate to the controller.

---

## 4. Layer 3: Controllers (`controllers/v1/property_controller.py`)

In Node.js and PHP MVC, controllers coordinate between HTTP and your application. They extract parameters, handle HTTP error statuses (like throwing `404 Not Found`), and call services.

### Code Sample:
```python
from uuid import UUID
from fastapi import HTTPException, status
from app.constants.messages import PROPERTY_NOT_FOUND
from app.services.v1 import property_service
from app.validations.v1.property_schema import PropertyCreate

class PropertyController:
    @staticmethod
    def get_property_by_id(property_id: UUID) -> dict:
        prop = property_service.get_by_id(property_id)
        if not prop:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=PROPERTY_NOT_FOUND
            )
        return prop

    @staticmethod
    def create_property(payload: PropertyCreate) -> dict:
        return property_service.create(payload)

property_controller = PropertyController()
```

### Line-by-Line Explanation:
- `class PropertyController:`:
  - Groups related endpoint actions together in one class (just like `PropertyController` in Express or PHP).
- `@staticmethod`:
  - In Python, a static method belongs to the class and doesn't require `self` (an instance state). You call it directly.
- `def get_property_by_id(property_id: UUID) -> dict:`:
  - Receives the UUID already validated by FastAPI.
- `prop = property_service.get_by_id(property_id)`:
  - Calls the Service layer to query data.
- `if not prop: raise HTTPException(...)`:
  - If the item does not exist, we raise an HTTP exception. FastAPI automatically converts this into a JSON response: `{"detail": "Property not found"}` with status code `404`.
- `property_controller = PropertyController()`:
  - Exports a singleton instance ready to be imported by routes.

---

## 5. Layer 4: Services (`services/v1/property_service.py`)

The Service layer contains **pure business logic**. It knows nothing about HTTP request objects or status codes. It only deals with data manipulation.

### Code Sample:
```python
from uuid import UUID, uuid4
from typing import Optional
from app.services.store import properties_db
from app.utils.datetime_utils import get_utc_now
from app.validations.v1.property_schema import PropertyCreate

class PropertyService:
    @staticmethod
    def create(data: PropertyCreate) -> dict:
        new_property = data.model_dump()
        new_property["id"] = uuid4()
        new_property["created_at"] = get_utc_now()
        properties_db.append(new_property)
        return new_property

    @staticmethod
    def get_by_id(property_id: UUID) -> Optional[dict]:
        for prop in properties_db:
            if prop["id"] == property_id:
                return prop
        return None

property_service = PropertyService()
```

### Line-by-Line Explanation:
- `new_property = data.model_dump()`:
  - In Pydantic v2, `.model_dump()` converts the Pydantic schema object into a native Python dictionary (`dict`, like a JavaScript object or PHP associative array).
- `new_property["id"] = uuid4()`:
  - Generates a cryptographically unique UUID4 for the property.
- `new_property["created_at"] = get_utc_now()`:
  - Attaches the current UTC timestamp using our helper in `app/utils`.
- `properties_db.append(new_property)`:
  - Appends the new record into the list (our mock database table). In Node, this is `properties.push(item)`. In PHP, `$properties[] = $item;`.
- `return new_property`:
  - Returns the newly created record.

---

## 6. Layer 5: Store (`services/store.py`)

This file is our mock database.

### Code:
```python
from typing import Dict, List

properties_db: List[Dict] = []
users_db: List[Dict] = []
```

### Explanation:
- `properties_db` and `users_db` are standard in-memory Python lists.
- When we add **SQLAlchemy** later, this file will be replaced with real database connection sessions and table models. Because our services only interact with data structures, swapping the store will be clean and effortless.

---

## 7. Layer 6: Router Aggregator (`routes/v1/__init__.py`)

This is the equivalent of Node's `routes/index.js` or Laravel's `routes/api.php`.

### Code:
```python
from fastapi import APIRouter
from .property_routes import router as property_router
from .user_routes import router as user_router

router = APIRouter()

router.include_router(property_router, prefix="/properties", tags=["Properties"])
router.include_router(user_router, prefix="/users", tags=["Users"])

__all__ = ["router"]
```

### Line-by-Line Explanation:
- `from .property_routes import router as property_router`:
  - Imports the property router. We use `as property_router` to avoid name collisions.
- `router.include_router(property_router, prefix="/properties", tags=["Properties"])`:
  - Mounts all routes inside `property_routes.py` with the `/properties` prefix.
  - `tags=["Properties"]` groups these endpoints under a clean collapsible "Properties" header in Swagger UI (`/docs`).
- `__all__ = ["router"]`:
  - Python convention: specifies what gets exported when another file imports from `app.routes.v1`.

---

## 8. Layer 7: Server Entrypoint (`app/main.py`)

The main bootstrap file of your FastAPI application (like `server.js` or `index.php`).

### Code:
```python
from fastapi import FastAPI
from app.config import settings
from app.routes.v1 import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Modular FastAPI REST API for Properties and Users",
)

app.include_router(api_v1_router)
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs"
    }
```

### Line-by-Line Explanation:
- `from app.config import settings`:
  - Loads application configuration (title, version, prefixes) from [`app/config/settings.py`](file:///home/c247/python/leanings/e-commerce/app/config/settings.py).
- `app = FastAPI(...)`:
  - Initializes the main web application instance.
- `app.include_router(api_v1_router)`:
  - Mounts our aggregated router. Both `/properties` and `/users` are immediately live.
- `app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)`:
  - Also mounts them under `/api/v1` (e.g. `/api/v1/properties`) for versioned API access.
- `@app.get("/")`:
  - Root healthcheck endpoint.

---

## Quick Reference Summary

| Layer | Node.js (Express) | PHP (Laravel) | FastAPI File | Role |
| :--- | :--- | :--- | :--- | :--- |
| **Routes** | `propertyRoutes.js` | `routes/api.php` | `app/routes/v1/property_routes.py` | URL mapping & HTTP decorators |
| **Validation** | Zod / Joi Schema | FormRequest | `app/validations/v1/property_schema.py` | Request parsing & type checks |
| **Controller** | `propertyController.js` | `PropertyController.php` | `app/controllers/v1/property_controller.py` | HTTP error codes & responses |
| **Service** | `propertyService.js` | `PropertyService.php` | `app/services/v1/property_service.py` | Business logic & data handling |
| **Database** | Prisma / Mongoose | Eloquent Model | `app/services/store.py` | In-memory store (later SQLAlchemy) |
| **Master Router**| `routes/index.js` | `RouteServiceProvider` | `app/routes/v1/__init__.py` | Aggregates all routes into one |
| **Entry Point** | `server.js` | `public/index.php` | `app/main.py` | Starts the app instance |
