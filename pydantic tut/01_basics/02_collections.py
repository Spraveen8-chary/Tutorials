from pydantic import BaseModel
from typing import List, Dict, Set, Optional

# Pydantic supports standard Python collection types for validation.
class Product(BaseModel):
    name: str
    price: float
    # List of strings
    tags: List[str] = []
    # Dictionary with string keys and integer values
    metadata: Dict[str, int] = {}
    # Set of integers (automatically handles uniqueness)
    unique_ids: Set[int] = set()

# Example usage
data = {
    "name": "Smartphone",
    "price": 699.99,
    "tags": ["electronics", "mobile", "tech"],
    "metadata": {"stock": 50, "warranty_months": 24},
    "unique_ids": [101, 102, 101, 103] # Note the duplicate 101
}

product = Product(**data)

print(f"Product: {product.name}")
print(f"Tags: {product.tags}")
print(f"Unique IDs: {product.unique_ids}") # Output will be {101, 102, 103}
