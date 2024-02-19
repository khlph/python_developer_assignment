from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from models import BrokerModel, UpdateBrokerModel
from pymongo import MongoClient, ReturnDocument

from bson import ObjectId
import os

# Get MongoDB server host from environment variable
mongo_server_host = os.environ.get("MONGO_SERVER_HOST", "localhost")

client = MongoClient(f"mongodb://{mongo_server_host}:27017/")
db = client["car_listing"]
brokers_collection = db["brokers"]

router = APIRouter(
  prefix='/brokers',
  tags = ['Broker']
)

@router.post(
  "/",
  response_description="Create a new broker",
  response_model=BrokerModel,
  status_code=status.HTTP_201_CREATED,
  response_model_by_alias=False,
)
async def create_broker(broker: BrokerModel):
  """
  Inserts a new broker into the database.
  """
  new_broker = brokers_collection.insert_one(broker.model_dump(by_alias=True, exclude=["id"]))
  created_broker = brokers_collection.find_one({"_id": new_broker.inserted_id})
  return created_broker

@router.get(
  "/{id}",
  response_description="Get a broker",
  response_model=BrokerModel,
  response_model_by_alias=False,
)
async def get_broker(id: str):
  """
  Get the record for a specific broker, looked up by `id`.
  """
  try:
    broker = brokers_collection.find_one({"_id": ObjectId(id)})
    if broker is not None:
      return broker
  except:
    raise HTTPException(status_code=404, detail=f"Broker {id} not found")

@router.put(
    "/{id}",
  response_description="Update a broker",
  response_model=BrokerModel,
  response_model_by_alias=False,
)
async def update_broker(id: str, broker: UpdateBrokerModel):
  """
  Update individual fields of an existing broker record.

  Only the provided fields will be updated.
  Any missing or `null` fields will be ignored.
  """
  broker = {
    k: v for k, v in broker.model_dump(by_alias=True).items() if v is not None
  }

  if len(broker) >= 1:
    update_result = brokers_collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": broker},
      return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
      return update_result
    else:
      raise HTTPException(status_code=404, detail=f"Broker {id} not found")

  # The update is empty, but we should still return the matching document:
  if (existing_broker := brokers_collection.find_one({"_id": id})) is not None:
    return existing_broker

  raise HTTPException(status_code=404, detail=f"Broker {id} not found")

@router.delete("/{id}", response_description="Delete a broker")
async def delete_broker(id: str):
  """
  Remove a single broker record from the database.
  """
  delete_result = brokers_collection.delete_one({"_id": ObjectId(id)})
  if delete_result.deleted_count == 1:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  raise HTTPException(status_code=404, detail=f"Broker {id} not found")
