import os
import json
import logging
from typing import List, Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, date

from models.manga import Manga

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()


def load_mangas() -> List[Manga]:
    """Load mangas from the JSON file."""
    if not os.path.exists(JSON_FILE_PATH):
        return []  # Return an empty list if the file does not exist
    with open(JSON_FILE_PATH, "r") as file:
        data = json.load(file)
        # Ensure we are creating Manga instances
        mangas = [Manga(**item) for item in data]
        return mangas  # Return a list of Manga instances


def save_mangas(mangas: List[Manga]):
    """Save the mangas list to the JSON file."""
    try:
        # Convert each Manga instance to a dictionary for JSON serialization
        mangas_dicts = [manga.model_dump() for manga in mangas]

        with open(JSON_FILE_PATH, "w") as file:
            json.dump(
                mangas_dicts, file, default=str, indent=4
            )  # Use indent for pretty printing
            logger.info("Saved mangas to JSON file.")
    except IOError as e:
        logger.error("Error saving manga data: %s", e)
        raise HTTPException(status_code=500, detail="Error saving manga data")


@app.get("/")
async def get_mangas():
    try:
        return load_mangas()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/manga/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/manga")
async def create_manga(manga: Manga):
    # Load existing mangas
    mangas = load_mangas()
    # Assign a new ID based on the existing mangas
    new_id = (mangas[-1].id + 1) if mangas else 1

    # Create a new Manga object with the new ID
    new_manga_data = manga.model_dump()  # Use model_dump() to convert to dict
    new_manga_data["id"] = new_id  # Add the new ID

    # Create a new Manga instance and append to the list
    new_manga = Manga(**new_manga_data)  # Validate before appending
    mangas.append(new_manga)  # Append the new Manga instance

    save_mangas(mangas)
    return new_manga


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Manga):
    return {"item_name": item.name, "item_id": item_id}
