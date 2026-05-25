from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    # 1. Alias: Useful when the input JSON has keys that are not valid Python identifiers
    # or follow a different naming convention (e.g., camelCase).
    title: str = Field(alias="book_title")
    
    # 2. Constraints: min_length, max_length, pattern (regex)
    isbn: str = Field(min_length=10, max_length=13)
    
    # 3. Numeric constraints: gt (greater than), lt (less than), ge (>=), le (<=)
    price: float = Field(gt=0, le=1000)
    
    # 4. Description and Metadata: Useful for documentation (like FastAPI Swagger)
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating from 0 to 5")

# Example data using the alias
input_data = {
    "book_title": "The Pydantic Guide",
    "isbn": "1234567890123",
    "price": 29.99,
    "rating": 4.5
}

book = Book(**input_data)

print(f"Title: {book.title}") # Access using the Python field name
print(f"ISBN: {book.isbn}")
print(f"Price: {book.price}")

# Converting back to dict can use aliases or field names
# print(f"\nDict with field names: {book.model_dump()}")
# print(f"Dict with aliases: {book.model_dump(by_alias=True)}")

# Validation failure example
try:
    Book(book_title="Short", isbn="123", price=-10, rating=6)
except Exception as e:
    print(f"\nCaught Expected Field Constraint Errors:\n{e}")
