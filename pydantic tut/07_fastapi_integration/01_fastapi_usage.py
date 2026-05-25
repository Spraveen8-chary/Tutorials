from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="Pydantic & FastAPI Tutorial")

# 1. Define Request Model
class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=100)
    price: float = Field(..., gt=0)
    tags: List[str] = []

# 2. Define Response Model
# Often we want to return more (or less) data than we receive (e.g., adding an ID)
class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    # We might exclude tags or description in some responses
    
# Mock Database
items_db = []

@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    # 'item' is already a validated Pydantic model instance here!
    new_id = len(items_db) + 1
    
    # Create the response data
    item_dict = item.model_dump()
    item_dict["id"] = new_id
    
    items_db.append(item_dict)
    
    # FastAPI will automatically validate 'item_dict' against 'ItemResponse'
    return item_dict

@app.get("/items/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    if item_id > len(items_db) or item_id < 1:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return items_db[item_id - 1]

if __name__ == "__main__":
    import uvicorn
    print("Run this file and go to http://127.0.0.1:8000/docs to see Pydantic in action with Swagger UI!")
    uvicorn.run(app, host="127.0.0.1", port=8000)
