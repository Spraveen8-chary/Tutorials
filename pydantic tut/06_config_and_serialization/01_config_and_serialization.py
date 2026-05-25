from pydantic import BaseModel, ConfigDict
import json

class UserProfile(BaseModel):
    # Configuration using ConfigDict (Pydantic V2)
    model_config = ConfigDict(
        # Allows using models with ORMs like SQLAlchemy (formerly orm_mode=True)
        from_attributes=True,
        # Trims whitespace from strings automatically
        str_strip_whitespace=True,
        # Prevents extra fields from being added to the model
        extra='forbid'
    )

    username: str
    bio: str

# 1. ORM Compatibility
# Mocking an ORM object (like a SQLAlchemy model instance)
class MockUserORM:
    def __init__(self, username, bio):
        self.username = username
        self.bio = bio

orm_user = MockUserORM(username="  john_doe  ", bio="Software Engineer")

# Create Pydantic model from ORM object
pydantic_user = UserProfile.model_validate(orm_user)
print(f"Validated from ORM: '{pydantic_user.username}' (Notice whitespace stripped)")

# 2. Serialization (Exporting data)
# To dictionary
user_dict = pydantic_user.model_dump()
print(f"\nModel as Dict: {user_dict}")

# To JSON string
user_json = pydantic_user.model_dump_json()
print(f"Model as JSON: {user_json}")

# 3. Forbid Extra Fields
try:
    UserProfile(username="alice", bio="coder", extra_field="not allowed")
except Exception as e:
    print(f"\nCaught Expected Extra Field Error:\n{e}")
