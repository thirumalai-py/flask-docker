from dotenv import load_dotenv
from flask_pymongo import PyMongo
from pymongo import MongoClient, DESCENDING
import certifi
import os

# Load environment variables from .env file
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

# Initialize the PyMongo instance (You can pass app object when creating app)
mongo = PyMongo()

# Connect the Mongo DB
client = MongoClient(
    mongo_uri, 
    tlsCAFile=certifi.where(),
    socketTimeoutMS=30000,  # Adjust socket timeout (default: 20000 ms)
    connectTimeoutMS=30000  # Adjust connection timeout (default: 20000 ms)
)

db = client['hv_ecommerce']