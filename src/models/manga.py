from datetime import date
from pydantic import BaseModel


class Manga(BaseModel):
    id: int
    name: str
    views: int
    authors: str
    rating: float
    url: str
    last_chapter: str
    last_chapter_release_date: date