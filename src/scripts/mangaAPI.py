from datetime import datetime
import manganelo
from typing import List, Union
from models.manga import Manga


class MangaManager:
    def __init__(self):
        pass

    def get_manga(self, title: str) -> Union[List[Manga], str]:
        try:
            results = manganelo.get_search_results(title)
            if not results:
                return "No results found."

            mangas = []
            for i, result in enumerate(results):
                manga = Manga(
                    id=i,
                    name=result.title,
                    views=result.views,
                    authors=", ".join(result.authors) if result.authors else "Unknown",
                    rating=result.rating if result.rating else 0.0,
                    url=result.url,
                    last_chapter=(
                        result.chapter_list[-1].url
                        if result.chapter_list
                        else "No chapters"
                    ),
                    # Convert last_chapter_release_date to a date object if it's a datetime
                    last_chapter_release_date=(
                        result.chapter_list[-1].uploaded.date()
                        if isinstance(result.chapter_list[-1].uploaded, datetime)
                        else result.chapter_list[-1].uploaded
                    ),
                )
                mangas.append(manga)

            return mangas
        except (IndexError, TypeError, AttributeError) as e:
            # Handle cases where the result or its fields are not as expected
            return f"Error retrieving data: {e}"


if __name__ == "__main__":
    m = MangaManager()
    result = m.get_manga("My Disciples Are All Big Villains")
    print(result)
