import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from main import app 

client = TestClient(app)

def test_car_api():
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
  car_id = response.json()["id"]

  # Send GET request to show all car
  response = client.get(f"/cars/")
  assert response.status_code == 200

  # Send GET request to retrieve the specific car
  response = client.get(f"/cars/{car_id}")
  assert response.status_code == 200
  assert response.json()['id'] == car_id

  # Send GET request with invalid car_id
  response = client.get(f"/cars/123")
  assert response.status_code == 404
  assert response.json()['detail'] == "Car 123 not found"

  # Send PUT request to update the specific car
  response = client.put(f"/cars/{car_id}", json={"mileage": 230000.1})
  assert response.status_code == 200
  assert response.json()['id'] == car_id
  assert response.json()['mileage'] == 230000.1

  # Send DELETE request to DELETE the specific car
  response = client.delete(f"/cars/{car_id}")
  assert response.status_code == 204

def test_broker_api():
  # TO:DO
  # - Add test for invalid email

  # Define test data
  broker_data = {
    "name": "John Doe",
    "email": "some@email.com",
    "phone_number": "0899999999",
    "address": "123 Bangkok"
  }
  
  # Send POST request to create a new broker
  response = client.post("/brokers/", json=broker_data)
  assert response.status_code == 201
  broker_id = response.json()["id"]
  
  # Send GET request to retrieve the specific broker
  response = client.get(f"/brokers/{broker_id}")
  assert response.status_code == 200
  assert response.json()['id'] == broker_id

  # Send PUT request to update the specific broker
  response = client.put(f"/brokers/{broker_id}", json={"email": "some1@email.com"})
  assert response.status_code == 200
  assert response.json()['id'] == broker_id
  assert response.json()['email'] == "some1@email.com"

  # Send DELETE request to DELETE the specific broker
  response = client.delete(f"/brokers/{broker_id}")
  assert response.status_code == 204

def test_listing_api():
  # Created Car and Broker before listing
  car_data = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2010,
    "color": "Blue",
    "mileage": 230000
  }
  broker_data = {
    "name": "John Doe",
    "email": "some@email.com",
    "phone_number": "0899999999",
    "address": "123 Bangkok"
  }

  car_response = client.post("/cars/", json=car_data)
  broker_response = client.post("/brokers/", json=broker_data)

  # Define test data
  listing_data = {
    "car_id": car_response.json()['id'],
    "broker_id": broker_response.json()['id'],
    "price": 200000,
    "description": "Mint Condition",
    "status": "ACTIVE",
  }

  # Send POST request to create a new listing
  response = client.post("/listing/", json=listing_data)
  assert response.status_code == 201
  assert response.json()['status'] == 'ACTIVE'
  listing_id = response.json()["id"]
  
  # Send PUT request to retrieve the specific listing
  response = client.put(f"/listing/{listing_id}", json={"status": "INACTIVE"})  
  assert response.status_code == 200
  assert response.json()['status'] == 'INACTIVE'

  # Send GET request to list a status of listing
  response = client.get("/listing?status=INACTIVE")
  assert response.status_code == 200

  # Send DELETE request to DELETE the specific listing
  response = client.delete(f"/listing/{listing_id}")
  assert response.status_code == 204
