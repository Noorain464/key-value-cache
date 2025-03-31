from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import asyncio
from cachetools import LRUCache
import psutil

app = FastAPI()
CACHE_SIZE = 100000
MEMORY_THRESHOLD = 70 

cache = LRUCache(maxsize=CACHE_SIZE)

class KeyValue(BaseModel):
    key: str
    value: str

async def memory_eviction():
    while True:
        memory_usage = psutil.virtual_memory().percent
        batch_size = int(CACHE_SIZE * (memory_usage - MEMORY_THRESHOLD) / 100)
        if memory_usage > MEMORY_THRESHOLD:
            print(f"Memory usage high ({memory_usage}%), evicting oldest items...")
            try:
                for _ in range(batch_size): 
                    cache.popitem()
                    print("Evicted 100 oldest cache items to reduce memory usage.")
            except KeyError:
                print("Cache is already empty.")
        await asyncio.sleep(1) 

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(memory_eviction()) 

@app.post("/put")
async def put_key_value(item: KeyValue):
    if len(item.key) > 256 or len(item.value) > 256:
        raise HTTPException(status_code=400, detail="Key/Value exceeds 256 characters")

    cache[item.key] = item.value
    return {"status": "OK", "message": "Key inserted/updated successfully."}

@app.get("/get")
async def get_key_value(key: str):
    if key in cache:
        return {"status": "OK", "key": key, "value": cache[key]}
    elif key not in cache: 
        return {"status": "ERROR", "message": "Key not found."}
    return {"status": "ERROR", "message": "Error description explaining what went wrong."}

