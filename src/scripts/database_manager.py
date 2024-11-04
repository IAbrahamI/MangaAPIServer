import sqlite3
import os
from typing import List
from src.scripts.mangaAPI import MangaManager
from models.manga import Manga


class DatabaseManager:
    def __init__(self):
        self.current_directory = os.path.dirname(__file__)
        self.db_name = "Mangas.db"
        self.db_directory = os.path.join(self.current_directory, "databases")
        self.db_path = os.path.join(self.db_directory, self.db_name)
        # Create the "databases" directory if it doesn't exist
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
            self._initialize_tables()
        # Connects to the database
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def _initialize_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS mangas (
                id INT PRIMARY KEY,
                name TEXT NOT NULL,
                views INT DEFAULT 0,
                authors TEXT,
                rating FLOAT,
                url TEXT NOT NULL,
                last_chapter TEXT,
                last_chapter_release_date DATE,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        self.conn.commit()

    def store_manga_data(self, manga_list: List[Manga]):
        for manga in manga_list:
            self.cursor.execute(
                """INSERT OR REPLACE INTO mangas (id, name, views, authors, rating, url, last_chapter, 
                last_chapter_release_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    manga.id,
                    manga.name,
                    manga.views,
                    manga.authors,
                    manga.rating,
                    manga.url,
                    manga.last_chapter,
                    manga.last_chapter_release_date
                ),
            )
        self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Instantiate managers
    manga_manager = MangaManager()
    db_manager = DatabaseManager()

    # Fetch manga data
    manga_list = manga_manager.search_for_title("My Disciples Are All Big Villains")

    if isinstance(manga_list, list):
        # Store in database
        db_manager.store_manga_data(manga_list)
    else:
        print(manga_list)  # Print error or "No results found."

    # Close the database connection
    db_manager.close()
