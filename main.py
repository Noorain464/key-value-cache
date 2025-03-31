from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import asyncio
from cachetools import LRUCache

# Initialize FastAPI app
app = FastAPI()

# Define cache size (based on memory limits)
CACHE_SIZE = 50000  # Tune this based on testing

# Use LRU Cache for memory-efficient storage
cache = LRUCache(maxsize=CACHE_SIZE)

# Define request model
class KeyValue(BaseModel):
    key: str
    value: str

# PUT: Store or update key-value pair
@app.post("/put")
async def put_key_value(item: KeyValue):
    if len(item.key) > 256 or len(item.value) > 256:
        raise HTTPException(status_code=400, detail="Key/Value exceeds 256 characters")

    cache[item.key] = item.value
    return {"status": "OK", "message": "Key inserted/updated successfully."}

# GET: Retrieve value for a given key
@app.get("/get")
async def get_key_value(key: str):
    if key in cache:
        return {"status": "OK", "key": key, "value": cache[key]}
    return {"status": "ERROR", "message": "Key not found."}

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "OK", "message": "Service is running."}

