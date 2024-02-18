from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

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