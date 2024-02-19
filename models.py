from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

# Nice reference
# https://fastapi.tiangolo.com/tutorial/extra-models/

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class CarModel(BaseModel):
  """
  Represents a car.
  """
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  brand: str = Field(...)
  model: str = Field(...)
  year: int = Field(...)
  color: str = Field(...)
  mileage: float = Field(...)

class UpdateCarModel(BaseModel):
  """
  A set of optional updates to be made to a document in the database.
  """
  brand: Optional[str] = None
  model: Optional[str] = None
  year: Optional[int] = None
  color: Optional[str] = None
  mileage: Optional[float] = None

class CarCollection(BaseModel):
  """
  A container holding a list of `Car` instances.
  """
  cars: List[CarModel]

class BrokerModel(BaseModel):
  """
  Represents a broker in the platform.
  """
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  name: str = Field(...)
  email: EmailStr = Field(...)
  phone_number: str = Field(...)
  address: str = Field(...)

class UpdateBrokerModel(BaseModel):
  """
  A set of optional updates to be made to a document in the database.
  """
  name: Optional[str] = None
  email: Optional[EmailStr] = None
  phone_number: Optional[str] = None
  address: Optional[str] = None

class ListingModel(BaseModel):
  """
  Represents a listing.
  """
  id: Optional[PyObjectId] = Field(alias="_id", default=None)
  price: float = Field(...)
  description: str = Field(...)
  status: str = Field(...)

  @field_validator('status')
  @classmethod
  def validate_status(cls, value):
    allowed_statuses = ["INACTIVE", "ACTIVE", "SOLD"]
    if value.upper() not in allowed_statuses:
      raise ValueError(f"Invalid status. Must be one of: {allowed_statuses}")
    return value

class ListingModelInDB(ListingModel):
  """
  Represents a listing in the database.
  """
  car_id: PyObjectId
  broker_id: PyObjectId

class UpdateListingModel(BaseModel):
  """
  A set of optional updates to be made to a document in the database.
  """
  price: Optional[float] = None
  description: Optional[str] = None
  status: Optional[str] = Field(...)

class ListingCollection(BaseModel):
  """
  A container holding a list of `Listing` instances.
  """
  cars: List[ListingModel]
