from app.src.models.manga import Manga
from app.src.scripts.database_manager import DatabaseManager
from app.src.scripts.mangaAPI_Demonicscans import MangaManager

class ServiceHandler:
    def __init__(self):
        self.manga_manager = MangaManager()
    
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
        
    # To be defined
    def update_all_entries(self):
        results = []
        with DatabaseManager() as db_manager:
            mangas = db_manager.get_all()
            for manga in mangas:
                manga_fetched = self.manga_manager.get_manga(manga[2])
                if isinstance(manga_fetched, Manga):
                    result = db_manager.store_manga_data(manga_fetched)
                    results.append(result)
                else:
                    results.append(f"No results found for {manga[2]}.")
        return results