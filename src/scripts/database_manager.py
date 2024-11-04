from datetime import datetime
import sqlite3
import os
from typing import List
from src.scripts.mangaAPI import MangaManager
from src.models.manga import Manga


# Define a date adapter and converter
def adapt_datetime(dt: datetime) -> str:
    return dt.isoformat()  # Convert datetime to ISO format string


def convert_datetime(iso_string: str) -> datetime:
    return datetime.fromisoformat(iso_string)  # Convert ISO string back to datetime


# Register the adapter and converter
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("datetime", convert_datetime)


class DatabaseManager:
    def __init__(self):
        self.current_directory = os.path.dirname(
            os.path.dirname(os.path.dirname(__file__))
        )
        self.db_name = "Mangas.db"
        self.db_directory = os.path.join(
            self.current_directory, "databases"
        )  # databases folder at project root
        self.db_path = os.path.join(self.db_directory, self.db_name)
        # Create the "databases" directory if it doesn't exist
        if not os.path.exists(self.db_directory):
            os.makedirs(self.db_directory)
        # Connects to the database
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
        self.cursor = self.conn.cursor()

        # Check if tables have been initialized
        if not hasattr(DatabaseManager, "tables_initialized"):
            self._initialize_tables()
            DatabaseManager.tables_initialized = True  # Set the flag

    def _initialize_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS mangas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Use AUTOINCREMENT for automatic ID generation
                name TEXT NOT NULL,
                views INT DEFAULT 0,
                authors TEXT,
                rating REAL,
                url TEXT NOT NULL,
                last_chapter TEXT,
                last_chapter_release_date datetime, 
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        )
        self.conn.commit()

    def _manga_exists(self, manga_name: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM mangas WHERE name = ?", (manga_name,))
        count = self.cursor.fetchone()[0]
        return count > 0  # Returns True if the manga exists

    def store_manga_data(self, manga: Manga):
        if not self._manga_exists(manga.name):
            self.cursor.execute(
                """INSERT OR REPLACE INTO mangas (name, views, authors, rating, url, last_chapter, 
                last_chapter_release_date) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    manga.name,
                    manga.views,
                    manga.authors,
                    manga.rating,
                    manga.url,
                    manga.last_chapter,
                    manga.last_chapter_release_date,
                ),
            )
        self.conn.commit()

    def remove_manga_data(self, manga_name: str):
        if self._manga_exists(manga_name):
            self.cursor.execute("""DELETE FROM mangas WHERE name = ?""", (manga_name,))
            self.conn.commit()

    def close(self):
        self.conn.close()


if __name__ == "__main__":
    # Instantiate managers
    manga_manager = MangaManager()
    db_manager = DatabaseManager()

    # Fetch manga data
    manga = manga_manager.get_manga("HxH")

    if isinstance(manga, Manga):
        # Store in database
        db_manager.store_manga_data(manga)
    else:
        print(manga)  # Print error or "No results found."

    db_manager.remove_manga_data("Reborn As The Heavenly")
    # Close the database connection
    db_manager.close()
