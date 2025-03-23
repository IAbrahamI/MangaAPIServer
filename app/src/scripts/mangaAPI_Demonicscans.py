import requests
from bs4 import BeautifulSoup
from datetime import datetime
from app.src.models.manga import Manga
from urllib.parse import quote

class MangaManager:
    def __init__(self):
        # Base URL for searching manga
        self.base_url = "https://demonicscans.org"
        
    def get_manga(self, manga_name: str) -> Manga:
        """Search for the manga and extract its details."""
        try:
            # Format the search URL due to characters being encripted twice on the url
            processed_manga_name = manga_name.replace(" ", "-")
            processed_manga_name = quote(processed_manga_name, safe="-")
            processed_manga_name = quote(processed_manga_name, safe="-")
            
            # Fetch the search result url
            search_url = f"{self.base_url}/manga/{processed_manga_name}"
            
            # Fetch the search results page
            search_response = requests.get(search_url)
            search_response.raise_for_status()
            search_soup = BeautifulSoup(search_response.text, 'html.parser')
            
            # Initialize data variables
            image_link = "No link found"
            authors = "No author found"
            status = "No status found"
            genres = []
            views = "0.0"
            rating = 0.0
            description = "Description not found"
            last_chapter = "No chapter found"
            last_chapter_url = "No chapter URL found"
            last_chapter_release_date = None
            
            # Extract image link
            try:
                image_container = search_soup.select_one("div#manga-page div.center-align img")
                if image_container and image_container.get('src'):
                    image_link = image_container['src']
                else:
                    image_link = "No image link found"
            except Exception as e:
                print(f"Error parsing image link: {e}")
                image_link = "No image link found"
            
            # Extract author, rating, status, last update
            try:
                fields = {}
                manga_info_stats = search_soup.find('div', id='manga-info-stats')
                for row in manga_info_stats.find_all('div', class_='flex flex-row'):
                    items = row.find_all('li')
                    if len(items) >= 2:
                        label = items[0].text.strip()
                        value = items[1].text.strip()
                        fields[label] = value

                authors = fields.get("Author", "No author found")
                rating_str = fields.get("Rating", "0%").strip('%')
                rating = float(rating_str) / 100  # Convert percentage to a float between 0 and 1
                status = fields.get("Status", "No status found")
                last_chapter_release_date_str = fields.get("Last Update", None)
                last_chapter_release_date = (
                    datetime.strptime(last_chapter_release_date_str, '%Y-%m-%d')
                    if last_chapter_release_date_str else None
                )
            except Exception as e:
                print(f"Error parsing image link: {e}")
                authors = "No author found"
                rating = 0.0
                status = "No status found"
                last_chapter_release_date = None
                
            # Extract genres
            try:
                genres_container = search_soup.find('div', class_='genres-list')
                # Extract all <li> elements and store their text in a list
                genres = [li.text.strip() for li in genres_container.find_all('li')] if genres_container else []
            except Exception as e:
                print(f"Error parsing image link: {e}")
                genres = []
                
            # Extract description
            try:
                description_container = search_soup.find('div', class_='white-font')
                if description_container:
                    description = description_container.get_text(separator=' ', strip=True)
                else:
                    "No description found"
            except Exception as e:
                print(f"Error parsing image link: {e}")
                description = "No description found"
                
            # Extract last chapter data
            try:
                last_chapter_container = search_soup.find('div', id='chapters-container')
                if last_chapter_container:
                    a_tag = last_chapter_container.find('a')
                    if a_tag:
                        last_chapter = ''.join([str(content).strip() for content in a_tag.contents if isinstance(content, str)])
                        chapter_number = ''.join([char for char in last_chapter.split()[-1] if char.isdigit() or char == '.'])
                        last_chapter_url = f"{self.base_url}/title/{processed_manga_name}/chapter/{chapter_number}/1"
                    else:
                        last_chapter = "No last chapter found"
                        last_chapter_url = "No link to last chapter found"
                else:
                    last_chapter = "No last chapter found"
                    last_chapter_url = "No link to last chapter found"
            except Exception as e:
                print(f"Error parsing image link: {e}")
                last_chapter = "No last chapter found"
                last_chapter_url = "No link to last chapter found"
            
            # Return the populated Manga model
            return Manga(
                url=search_url,
                name=manga_name,
                image_link=image_link,
                authors=authors,
                status=status,
                genres=genres,
                views=views,
                rating=rating,
                description=description,
                last_chapter=last_chapter,
                last_chapter_url=last_chapter_url,
                last_chapter_release_date=last_chapter_release_date
            )
            
        except Exception as e:
            print(f"An error occurred: {e}")
            return None