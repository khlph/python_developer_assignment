from fastapi import APIRouter, HTTPException, status
from fastapi.responses import Response
from pydantic import ValidationError

from pymongo import MongoClient, ReturnDocument
from models import ListingModel, ListingModelInDB, UpdateListingModel, ListingCollection

from bson import ObjectId
import os

# Get MongoDB server host from environment variable
mongo_server_host = os.environ.get("MONGO_SERVER_HOST", "localhost")

client = MongoClient(f"mongodb://{mongo_server_host}:27017/")
db = client["car_listing"]
cars_collection = db["cars"]
brokers_collection = db["brokers"]
listing_collection = db["listing"]

router = APIRouter(
  prefix='/listing',
  tags = ['Listing']
)

@router.post("/",
  response_description="Create a listing, with car and broker exist",
  response_model=ListingModel,
  status_code=status.HTTP_201_CREATED,
  response_model_by_alias=False,
  )
async def create_listing(create_data: ListingModelInDB):
  try:
    # Ensure car and broker exist
    car = cars_collection.find_one({"_id": ObjectId(create_data.car_id)})
    broker = brokers_collection.find_one({"_id":ObjectId(create_data.broker_id)})
    if not car or not broker:
      raise HTTPException(
        status_code=400, detail="Invalid car or broker reference"
      )

    # Insert the new listing document (without full car/broker data)
    new_listing_id = listing_collection.insert_one(create_data.model_dump(exclude=["id"]))
    listing = listing_collection.find_one({"_id": new_listing_id.inserted_id})
    return listing
  except ValidationError as e:
    raise HTTPException(status_code=400, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}",
  response_description="Update a listing",
  response_model=ListingModel,
  response_model_by_alias=False,
  )
async def update_listing(id: str, listing: UpdateListingModel):
  """
  Update individual fields of an existing listing record.

  Only the provided fields will be updated.
  Any missing or `null` fields will be ignored.
  """
  listing = {
    k: v for k, v in listing.model_dump(by_alias=True).items() if v is not None
  }

  if len(listing) >= 1:
    update_result = listing_collection.find_one_and_update(
      {"_id": ObjectId(id)},
      {"$set": listing},
      return_document=ReturnDocument.AFTER,
    )
    if update_result is not None:
      return update_result
    else:
      raise HTTPException(status_code=404, detail=f"Listing {id} not found")

  # The update is empty, but we should still return the matching document:
  if (existing_listing := listing_collection.find_one({"_id": id})) is not None:
    return existing_listing

  raise HTTPException(status_code=404, detail=f"Listing {id} not found")


@router.get("/",
  response_description="List a listing by status",
  response_model=ListingCollection,
  response_model_by_alias=False,
  )
async def get_listings_by_status(status: str = "ACTIVE"):
  if status and status.upper() not in ["INACTIVE", "ACTIVE", "SOLD"]:
    raise HTTPException(
      status_code=404, detail="Invalid status"
    )
  query = {}  # Start with an empty query
  if status:
      query["status"] = status.upper()  # Fetch listings 
  return ListingCollection(cars=listing_collection.find(query))

@router.delete("/{id}", response_description="Delete a listing")
async def delete_listing(id: str):
  """
  Remove a single listing record from the database.
  """
  delete_result = listing_collection.delete_one({"_id": ObjectId(id)})
  if delete_result.deleted_count == 1:
    return Response(status_code=status.HTTP_204_NO_CONTENT)

  raise HTTPException(status_code=404, detail=f"Listing {id} not found")