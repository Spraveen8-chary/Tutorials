from pydantic import BaseModel, field_validator, model_validator
from typing import Optional

class UserRegistration(BaseModel):
    username: str
    password: str
    confirm_password: str
    age: int

    # 1. Field Validator: Validates a specific field
    # The method must be a class method and take 'cls', 'v' (the value)
    @field_validator('username')
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v

    @field_validator('age')
    @classmethod
    def age_limit(cls, v: int) -> int:
        if v < 18:
            raise ValueError('Must be at least 18 years old')
        return v

    # 2. Model Validator (Root Validator): Validates multiple fields together
    # In Pydantic V2, use @model_validator(mode='after') to validate after fields are initialized
    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UserRegistration':
        pw1 = self.password
        pw2 = self.confirm_password
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self

# Examples
try:
    # This will pass
    valid_user = UserRegistration(
        username="user123",
        password="secretpassword",
        confirm_password="secretpassword",
        age=25
    )
    print("User validated successfully!")
except ValueError as e:
    print(f"Validation Error: {e}")

try:
    # This will fail: password mismatch and age < 18
    invalid_user = UserRegistration(
        username="user 123", # Not alphanumeric
        password="pwd1",
        confirm_password="pwd2",
        age=16
    )
except ValueError as e:
    print(f"\nCaught Expected Validation Errors:\n{e}")
