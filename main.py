import os
import json
import logging
from typing import List, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date

from src.models.manga import Manga

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def get_mangas():
    pass


@app.get("/manga/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/manga")
async def create_manga(manga: Manga):
    pass


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Manga):
    pass
