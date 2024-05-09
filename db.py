from pymongo import MongoClient

# initialize mongo client
client = MongoClient('mongodb://localhost:27017/')
db = client['movies']

# Initialize database
movies_collection = db['movies']