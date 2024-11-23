from datetime import datetime
from pydantic import BaseModel


class Manga(BaseModel):
    name: str
    views: int
    authors: str
    rating: float
    url: str
    last_chapter: str
    last_chapter_release_date: datetime