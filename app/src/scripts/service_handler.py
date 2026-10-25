import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor

from app.src.models.manga import Manga
from app.src.scripts.database_manager import DatabaseManager
from app.src.scripts.mangaAPI_Demonicscans import MangaManager

logger = logging.getLogger(__name__)

# Number of mangas scraped in parallel
SCRAPE_WORKERS = 4

class ServiceHandler:
    def __init__(self):
        self.manga_manager = MangaManager()
        # Ensures only one full scrape runs at a time
        self._scrape_lock = threading.Lock()
        self._last_results = []
    
    def create_entry(self, manga_name: str):
        manga_fetched = self.manga_manager.get_manga(manga_name)
        if isinstance(manga_fetched, Manga):
            with DatabaseManager() as db_manager:
                result = db_manager.store_manga_data(manga_fetched)
                return result
        else:
            return f"No results found for {manga_name}."
        
    def retrieve_manga(self, manga_name: str):
        with DatabaseManager() as db_manager:
            manga = db_manager.get_manga(manga_name)
            return manga
        
    def get_all_entries(self):
        with DatabaseManager() as db_manager:
            mangas = db_manager.get_all()
            return mangas
        
    def remove_manga(self, manga_name: str):
        with DatabaseManager() as db_manager:
            db_manager.remove_manga_data(manga_name)
            return "Manga removed successfully"
        
    def update_all_entries(self, trigger: str = "manual"):
        """Scrape all mangas. If a scrape is already running, wait for it and return its results."""
        if not self._scrape_lock.acquire(blocking=False):
            logger.info("Scrape already running, waiting for it (trigger=%s)", trigger)
            with self._scrape_lock:
                return self._last_results
        try:
            self._last_results = self._scrape_all(trigger)
            return self._last_results
        finally:
            self._scrape_lock.release()

    def _scrape_all(self, trigger: str):
        logger.info("Scrape started (trigger=%s)", trigger)
        start = time.monotonic()
        with DatabaseManager() as db_manager:
            names = [manga[2] for manga in db_manager.get_all()]
        # Scrape without holding a DB connection, so other requests are not blocked
        with ThreadPoolExecutor(max_workers=SCRAPE_WORKERS) as pool:
            fetched = list(pool.map(self.manga_manager.get_manga, names))
        results = []
        with DatabaseManager() as db_manager:
            for name, manga_fetched in zip(names, fetched):
                if isinstance(manga_fetched, Manga):
                    results.append(db_manager.store_manga_data(manga_fetched))
                else:
                    results.append(f"No results found for {name}.")
        ok = sum(isinstance(manga, Manga) for manga in fetched)
        logger.info(
            "Scrape finished (trigger=%s): %d ok, %d failed in %.1fs",
            trigger, ok, len(names) - ok, time.monotonic() - start,
        )
        return results