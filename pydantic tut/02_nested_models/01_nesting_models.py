from pydantic import BaseModel
from typing import List

# 1. Define the Child Model
class Image(BaseModel):
    url: str
    name: str

# 2. Define the Parent Model that uses the Child Model
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    
    # Nesting: A single model instance
    image: Image = None
    
    # Nesting: A list of model instances
    alternative_images: List[Image] = []

# Example data representing a complex JSON object
item_data = {
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "image": {
        "url": "http://example.com/main.jpg",
        "name": "main_image"
    },
    "alternative_images": [
        {"url": "http://example.com/side.jpg", "name": "side_view"},
        {"url": "http://example.com/back.jpg", "name": "back_view"}
    ]
}

# Pydantic recursively validates all nested models
item = Item(**item_data)

print(f"Item Name: {item.name}")
print(f"Main Image URL: {item.image.url}")
print(f"Number of Alt Images: {len(item.alternative_images)}")
print(f"First Alt Image Name: {item.alternative_images[0].name}")
