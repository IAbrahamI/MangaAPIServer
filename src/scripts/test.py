"""from src.scripts.database_manager import DatabaseManager
from src.scripts.mangaAPI import MangaManager


manga_manager = MangaManager()
manga = manga_manager.get_manga("Reincarnated In A Cursed Game")

#with DatabaseManager() as db_manager:
#    db_manager.store_manga_data(manga)

with DatabaseManager() as db_manager:
    print(db_manager.get_all())"""
    
from src.scripts.service_handler import ServiceHandler

s_handler = ServiceHandler()

print(s_handler.get_all_entries())