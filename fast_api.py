from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()

# In-memory dictionary database
inventory = {
    1: {
        "make": "KTM",
        "model": "RT90",
        "year": 2021
    },
    2: {
        "make":"Yamaha",
        "model":"rx100",
        "year":2000
    }
}

# -------------------------------------------------------------
# Pydantic Schemas
# -------------------------------------------------------------
# Schema for creation (POST) and complete replacement (PUT)
class Item(BaseModel):
    make: str = Field(..., min_length=1, description="Brand or manufacturer")
    model: str = Field(..., min_length=1, description="Model identifier")
    year: int = Field(..., ge=1900, le=2026, description="Year of manufacture")

# Schema for partial updates (PATCH) - all fields are optional
class ItemPatch(BaseModel):
    make: str | None = Field(default=None, min_length=1, description="Brand or manufacturer")
    model: str | None = Field(default=None, min_length=1, description="Model identifier")
    year: int | None = Field(default=None, ge=1900, le=2026, description="Year of manufacture")


# -------------------------------------------------------------
# Informational Routes
# -------------------------------------------------------------
@app.get("/")
def home():
    return {"data": "hello.."}


@app.get("/about")
def about():
    return {"about": "data"}


# -------------------------------------------------------------
# GET Endpoints
# -------------------------------------------------------------
@app.get("/get-item/{item_id}")
def get_item_by_id(item_id: int):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return inventory[item_id]


@app.get("/get-by-name/{item_name}")
def get_item_by_name(item_name: str):
    for item in inventory.values():
        if item["make"].lower() == item_name.lower():
            return item
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item '{item_name}' not found"
    )


# -------------------------------------------------------------
# POST Endpoint (Create)
# -------------------------------------------------------------
@app.post("/insert-item/", status_code=status.HTTP_201_CREATED)
def create_item_auto_id(item: Item):
    new_id = max(inventory.keys()) + 1 if inventory else 1
    inventory[new_id] = item.model_dump()
    return {"item_id": new_id, "data": inventory[new_id]}


# -------------------------------------------------------------
# PUT Endpoint (Full Replacement / Update)
# -------------------------------------------------------------
@app.put("/update-item/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Item):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} cannot be updated because it does not exist."
        )

    inventory[item_id] = item.model_dump()
    return {
        "message": f"Item {item_id} updated successfully",
        "updated_item": inventory[item_id]
    }


# -------------------------------------------------------------
# PATCH Endpoint (Partial Update)
# -------------------------------------------------------------
@app.patch("/patch-item/{item_id}", status_code=status.HTTP_200_OK)
def patch_item(item_id: int, item: ItemPatch):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    # Extract only fields provided in the request body
    patch_data = item.model_dump(exclude_unset=True)

    if not patch_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields provided to update"
        )

    inventory[item_id].update(patch_data)
    return {
        "message": f"Item {item_id} partially updated",
        "updated_item": inventory[item_id]
    }


# -------------------------------------------------------------
# DELETE Endpoint (Remove)
# -------------------------------------------------------------
@app.delete("/delete-item/{item_id}", status_code=status.HTTP_200_OK)
def delete_item(item_id: int):
    if item_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} does not exist"
        )
    
    deleted_item = inventory.pop(item_id)
    return {
        "message": f"Item {item_id} deleted successfully",
        "deleted_data": deleted_item
    }