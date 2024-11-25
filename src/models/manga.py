from pydantic import BaseModel
from datetime import datetime
from typing import List

class Manga(BaseModel):
    url: str
    name: str
    authors: str
    status: str
    genres: List[str]
    views: str
    rating: float
    description: str
    last_chapter: str
    last_chapter_url: str
    last_chapter_release_date: datetime