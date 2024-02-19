from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from models import CarModel, UpdateCarModel, CarCollection
from pymongo import MongoClient, ReturnDocument

from bson import ObjectId
import os

# Get MongoDB server host from environment variable
mongo_server_host = os.environ.get("MONGO_SERVER_HOST", "localhost")

client = MongoClient(f"mongodb://{mongo_server_host}:27017/")
db = client["car_listing"]
cars_collection = db["cars"]

router = APIRouter(
  prefix='/cars',
  tags = ['Car']
)

@router.post(
  "/",
  response_description="Create a new car",
  response_model=CarModel,
  status_code=status.HTTP_201_CREATED,
  response_model_by_alias=False,
)
async def create_car(car: CarModel):
  """
  Inserts a new car into the database.
  """
  new_car = cars_collection.insert_one(car.model_dump(by_alias=True, exclude=["id"]))
  created_car = cars_collection.find_one({"_id": new_car.inserted_id})
  return created_car

@router.get(
  "/",
  response_description="List all cars",
  response_model=CarCollection,
  response_model_by_alias=False,
)
async def list_cars():
  """
  List all of the cars data in the database.
  The response is unpaginated.
  """
  return CarCollection(cars=cars_collection.find())

@router.get(
  "/{id}",
  response_description="Get a car",
  response_model=CarModel,
  response_model_by_alias=False,
)
async def get_car(id: str):
  """
  Get the record for a specific car, looked up by `id`.
  """
  try:
    car = cars_collection.find_one({"_id": ObjectId(id)})
    if car is not None:
      return car
  except:
    raise HTTPException(status_code=404, detail=f"Car {id} not found")

@router.put(
    "/{id}",
  response_description="Update a car",
  response_model=CarModel,
  response_model_by_alias=False,
)
async def update_car(id: str, car: UpdateCarModel):
  """
  Update individual fields of an existing car record.

  Only the provided fields will be updated.
  Any missing or `null` fields will be ignored.
  """
  car = {
    k: v for k, v in car.model_dump(by_alias=True).items() if v is not None
  }

  if len(car) >= 1:
    update_result = cars_collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": car},
      return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
      return update_result
    else:
      raise HTTPException(status_code=404, detail=f"Car {id} not found")

  # The update is empty, but we should still return the matching document:
  if (existing_car := cars_collection.find_one({"_id": id})) is not None:
    return existing_car

  raise HTTPException(status_code=404, detail=f"Car {id} not found")

@router.delete("/{id}", response_description="Delete a car")
async def delete_car(id: str):
  """
  Remove a single car record from the database.
  """
  delete_result = cars_collection.delete_one({"_id": ObjectId(id)})
  if delete_result.deleted_count == 1:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  raise HTTPException(status_code=404, detail=f"Car {id} not found")
