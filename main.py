from fastapi import FastAPI
from routers import brokers, cars, listing

app = FastAPI()
app.include_router(brokers.router)
app.include_router(cars.router)
app.include_router(listing.router)