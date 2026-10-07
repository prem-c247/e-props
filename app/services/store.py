from typing import Dict, List

# In-memory database tables (simulating database collections)
# When we transition to SQLAlchemy later, these will be replaced with real DB models & sessions.
properties_db: List[Dict] = []
users_db: List[Dict] = []
