import json
from pymongo import MongoClient


# MongoDB connection string

MONGO_URI = "mongodb+srv://wbltrn_db_user:qTLPo6zOsDGUeYSr@movie-rental-project.klyxbtn.mongodb.net/?appName=movie-rental-project"

client = MongoClient(MONGO_URI)

db = client["movie_rental_dw"]
collection = db["customer_loyalty"]


# Load JSON file

with open("data/exports/dim_customer_loyalty.json", "r") as file:
    data = json.load(file)


# Insert into MongoDB

collection.insert_many(data)

print("Data successfully inserted into MongoDB!")
