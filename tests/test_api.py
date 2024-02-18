import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from main import app 

client = TestClient(app)

# Connect to MongoDB
db_client = MongoClient("mongodb://localhost:27017/")
db = db_client["car_listing"]
cars_collection = db["cars"]

def test_create_car():
  # Define test data
  car_data = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2010,
    "color": "Blue",
    "mileage": 230000
  }

  # Send POST request to create a new car
  response = client.post("/cars/", json=car_data)
  assert response.status_code == 201
  cars_collection.delete_many({})

def test_list_car():
  # Insert test data into the database
  car_data = {"brand": "Toyota", "model": "Corolla", "year": 2018, "color": "Black", "mileage": 18000.0}
  cars_collection.insert_one(car_data)

  # Send GET request to show all car
  response = client.get(f"/cars/")
  assert response.status_code == 200
  assert len(response.json()['cars']) == 1
  cars_collection.delete_many({})

def test_get_car():
  car_data = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2010,
    "color": "Blue",
    "mileage": 230000
  }
  insert_car = cars_collection.insert_one(car_data)
  car_id = str(insert_car.inserted_id)

  # Send GET request to retrieve the specific car
  response = client.get(f"/cars/{car_id}")
  assert response.status_code == 200
  assert response.json()['id'] == car_id
  cars_collection.delete_many({})

def test_get_car_not_found():

  # Send GET request with invalid car_id
  response = client.get(f"/cars/123")
  assert response.status_code == 404
  assert response.json()['detail'] == "Car 123 not found"

def test_update_car():
  # Insert test data into the database
  car_data = {"brand": "Toyota", "model": "Corolla", "year": 2018, "color": "Black", "mileage": 18000.0}
  insert_car = cars_collection.insert_one(car_data)
  car_id = str(insert_car.inserted_id)

  # Send GET request to retrieve the specific car
  response = client.put(f"/cars/{car_id}", json={"mileage": 18001.1})
  assert response.status_code == 200
  assert response.json()['id'] == car_id
  assert response.json()['id'] == 18001.1
  cars_collection.delete_many({})

def test_delete_car():
  # Insert test data into the database
  car_data = {"brand": "Toyota", "model": "Corolla", "year": 2018, "color": "Black", "mileage": 18000.0}
  insert_car = cars_collection.insert_one(car_data)
  car_id = str(insert_car.inserted_id)

  # Send GET request to retrieve the specific car
  response = client.delete(f"/cars/{car_id}")
  assert response.status_code == 204