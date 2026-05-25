from pydantic import BaseModel
from typing import Optional

# 1. Defining a basic Pydantic Model
# Pydantic models are classes that inherit from BaseModel.
# They define the schema of your data.
class User(BaseModel):
    # Required fields: No default value provided
    id: int
    username: str
    
    # Optional fields: Use Optional type hint and provide a default value (None)
    email: Optional[str] = None
    
    # Field with a default value
    is_active: bool = True

# 2. Creating an instance of the Model
# Data is passed as keyword arguments.
user_data = {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
}

user = User(**user_data)

# 3. Accessing data
print(f"User ID: {user.id}")
print(f"Username: {user.username}")
print(f"Is Active: {user.is_active}")

# 4. Validation in action
try:
    # This will fail because 'id' is required and missing, and 'id' should be an int
    invalid_user = User(username="bad_user")
except Exception as e:
    print(f"\nValidation Error (missing 'id'):\n{e}")

try:
    # Pydantic attempts to coerce types (e.g., string "123" to int 123)
    coerced_user = User(id="123", username="coerced_user")
    print(f"\nCoerced ID: {coerced_user.id} (Type: {type(coerced_user.id)})")
except Exception as e:
    print(e)
