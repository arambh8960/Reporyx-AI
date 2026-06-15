"""
MongoDB Database Connection
Handles async MongoDB connection using Motor
"""

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

# Global MongoDB client
client: AsyncIOMotorClient = None
database = None


async def connect_to_mongo():
    """
    Establish connection to MongoDB
    """
    global client, database
    
    mongodb_url = os.getenv("MONGODB_URL")
    
    if not mongodb_url:
        raise ValueError("MONGODB_URL environment variable is not set")
    
    client = AsyncIOMotorClient(mongodb_url)
    
    # Test connection
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
        
        # Get database (using 'codegraph_ai' as database name)
        database = client.codegraph_ai
        
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection
    """
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    """
    Get database instance
    """
    if database is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return database


def get_collection(collection_name: str):
    """
    Get a specific collection from the database
    """
    db = get_database()
    return db[collection_name]
