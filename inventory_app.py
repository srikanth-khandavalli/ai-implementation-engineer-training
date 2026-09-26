from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
app = FastAPI()
#in-memory dictionary Data Base
inventory = {
    1:{
        "make":"KTM",
        "model":"390 Duke",
        "year":2025
    },
    2:{
        "make":"yamaha",
        "model":"R15",
        "year":2024
    }

}
class vehicle(BaseModel):
    make: str 
    model: str
    year: int 


@app.get("/about")
def about():
    return {"about":"This is a Inventory management system!"}

@app.get("/")
def root():
    return {"intro":"Hello! How are you today?"}

# http:120.0.0.1:8000/get-vehicle/1

@app.get("/get-vehicle/{vehicle_id}")
def get_vehicle(vehicle_id: int):
    if vehicle_id not in inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"vehicle:{vehicle_id} not found"
        )
    return inventory[vehicle_id]
# post End point (create new record)
@app.post("/insert/", status_code=status.HTTP_201_CREATED)
def create_item(item:vehicle):
    new_id = max(inventory.keys()) + 1 if inventory else 1
    inventory[new_id]=item.model_dump()
    return {"item_id":new_id, "data":inventory[new_id]}


# put end point to update the record
@app.put("/update/{item_id}", status_code=status.HTTP_200_OK)
def update_item(item_id:int, item:vehicle):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    inventory[item_id]=item.model_dump()
    return {
        "message":f"item {item_id} updated..",
        "updated_item":inventory[item_id]
    }