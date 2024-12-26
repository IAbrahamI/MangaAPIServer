from datetime import datetime
import sqlite3
import os
from typing import List
from app.src.models.manga import Manga


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
        # Initialize the connection and cursor
        self.conn = None
        self.cursor = None    
        
    def connect(self):
        """Open the database connection."""
        self.conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        # Register the custom converter
        sqlite3.register_converter("datetime", self._convert_datetime)
        self.cursor = self.conn.cursor()

    @staticmethod
    def _convert_datetime(value):
        """Custom converter to handle both timestamp and DATETIME formats."""
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        # Try to parse as standard DATETIME format (YYYY-MM-DD HH:MM:SS)
        try:
            parsed_datetime = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            # Return the datetime formatted as a string in the desired format
            return parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Try to parse ISO format "YYYY-MM-DDTHH:MM:SS"
            try:
                parsed_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                # Return the datetime formatted as a string in the desired format
                return parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                raise ValueError(f"Unrecognized datetime format: {value}")

    def _initialize_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS mangas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                name TEXT NOT NULL,
                image_link TEXT NOT NULL,
                authors TEXT NOT NULL,
                status TEXT NOT NULL,
                genres TEXT NOT NULL,  -- List of strings, will store as comma-separated values
                views TEXT NOT NULL,
                rating REAL NOT NULL,
                description TEXT NOT NULL,
                last_chapter TEXT NOT NULL,
                last_chapter_url TEXT NOT NULL,
                last_chapter_release_date TEXT NOT NULL
            )"""
        )
        self.conn.commit()

    def _manga_exists(self, manga_name: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) FROM mangas WHERE name = ?", (manga_name,))
        count = self.cursor.fetchone()[0]
        return count > 0  # Returns True if the manga exists

    def store_manga_data(self, manga: Manga):
        """Insert or update manga data in the database, now including `image_link`."""
        if not self._manga_exists(manga.name):
            # Convert genres list to a comma-separated string
            genres_str = ', '.join(manga.genres)
            self.cursor.execute(
                '''INSERT INTO mangas (
                    url, name, image_link, authors, status, genres, views, rating, 
                    description, last_chapter, last_chapter_url, 
                    last_chapter_release_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    manga.url,
                    manga.name,
                    manga.image_link,
                    manga.authors,
                    manga.status,
                    genres_str,
                    manga.views,
                    manga.rating,
                    manga.description,
                    manga.last_chapter,
                    manga.last_chapter_url,
                    manga.last_chapter_release_date
                )
            )
            self.conn.commit()
            return f"Manga: {manga.name} stored successfully."
        else:
            # If manga exists, update the existing record
            genres_str = ', '.join(manga.genres)  # Convert genres list to a comma-separated string
            self.cursor.execute(
                '''UPDATE mangas 
                SET image_link = ?,
                    authors = ?, 
                    status = ?, 
                    genres = ?, 
                    views = ?, 
                    rating = ?, 
                    description = ?, 
                    last_chapter = ?, 
                    last_chapter_url = ?, 
                    last_chapter_release_date = ?
                WHERE name = ?''', 
                (
                    manga.image_link,
                    manga.authors,
                    manga.status,
                    genres_str,
                    manga.views,
                    manga.rating,
                    manga.description,
                    manga.last_chapter,
                    manga.last_chapter_url,
                    manga.last_chapter_release_date,
                    manga.name  # Use the unique identifier (e.g., name or URL)
                )
            )
            self.conn.commit()
            return f"Manga: {manga.name} updated successfully."

    def remove_manga_data(self, manga_name: str):
        if self._manga_exists(manga_name):
            self.cursor.execute("""DELETE FROM mangas WHERE name = ?""", (manga_name,))
            self.conn.commit()

    def get_manga(self, manga_name: str):
        if self._manga_exists(manga_name):
            self.cursor.execute("SELECT * FROM mangas WHERE name = ?", (manga_name,))
            result = self.cursor.fetchone()
            return result
        else:
            return "No manga found with that name."
        
    def get_all(self):
        self.cursor.execute("SELECT * FROM mangas")
        result = self.cursor.fetchall()
        return result

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            
    def __enter__(self):
        self.connect()  # Connect when entering the context
        # Check if tables have been initialized
        if not hasattr(DatabaseManager, "tables_initialized"):
            self._initialize_tables()
            DatabaseManager.tables_initialized = True  # Set the flag
        return self  # Return the instance to be used inside the 'with' block

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()  # Close the connection when exiting the context