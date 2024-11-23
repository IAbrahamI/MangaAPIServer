from src.models.manga import Manga
from src.scripts.database_manager import DatabaseManager
from src.scripts.mangaAPI import MangaManager

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
        
    # To be defined
    def update_all_entries(self):
        pass
            
