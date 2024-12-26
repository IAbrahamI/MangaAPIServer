import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.models.manga import Manga

class MangaManager:
    def __init__(self):
        # Base URL for searching manga
        self.base_url = "https://manganato.com/search/story/"

    def get_manga(self, manga_name: str) -> Manga:
        """Search for the manga and extract its details."""
        try:
            # Format the search URL
            processed_manga_name = manga_name.lower().replace(" ", "_")
            search_url = f"{self.base_url}{processed_manga_name}"

            # Fetch the search results page
            search_response = requests.get(search_url)
            search_response.raise_for_status()
            search_soup = BeautifulSoup(search_response.text, 'html.parser')

            # Find the first search result
            first_result = search_soup.select_one("div.panel-search-story div.search-story-item a")
            if not first_result:
                print("No results found.")
                return None
            
            # Extract the manga link
            href = first_result['href']

            # Fetch the manga details page
            details_response = requests.get(href)
            details_response.raise_for_status()
            details_soup = BeautifulSoup(details_response.text, 'html.parser')
 
            # Initialize data variables
            name = manga_name
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

            # Extract author
            try:
                author_tag = details_soup.select_one("td.table-value a[rel='nofollow']")
                if author_tag:
                    authors = author_tag.text.strip()
                else:
                    authors = "No author found"
            except Exception as e:
                print(f"Error parsing author: {e}")
                authors = "No author found"

            # Extract status
            try:
                status_tag = details_soup.select_one("td:-soup-contains('Status :') + td.table-value")
                if status_tag:
                    status = status_tag.text.strip()
                else:
                    status = "No status found"
            except Exception as e:
                print(f"Error parsing status: {e}")
                status = "No status found"

            # Extract genres
            try:
                genres_tag = details_soup.select_one("tr:-soup-contains('Genres') td.table-value")
                if genres_tag:
                    genre_links = genres_tag.find_all('a')
                    genres = [genre.text.strip() for genre in genre_links]
                else:
                    genres = []
            except Exception as e:
                print(f"Error parsing genres: {e}")
                genres = []


            # Extract views
            try:
                views_tag = details_soup.select_one("p span.stre-label:-soup-contains('View :') + span.stre-value")
                if views_tag:
                    views = str(views_tag.text.strip().replace(',', ''))
                else:
                    views = "No views found"
            except Exception as e:
                print(f"Error parsing views: {e}")
                views = "No views found"

            # Extract rating
            try:
                rating_tag = details_soup.select_one("em[property='v:average']")
                if rating_tag:
                    rating = float(rating_tag.text.strip())
                else:
                    rating = 0.0
            except Exception as e:
                print(f"Error parsing rating: {e}")
                rating = 0.0


            # Extract description
            try:
                description_container = details_soup.find("div", class_="panel-story-info-description")
                if description_container:
                    # Get all the text content but exclude the <h3>
                    description_text = ''.join(
                        description_container.find_all(string=True, recursive=False)
                    ).strip()
                    description = description_text
                else:
                    description = "Description not found"
            except Exception as e:
                print(f"Error parsing description: {e}")
                description = "Description not found"

            # Extract the latest chapter
            try:
                latest_chapter_tag = details_soup.select_one("ul.row-content-chapter a.chapter-name.text-nowrap")
                if latest_chapter_tag:
                    last_chapter = latest_chapter_tag.text.strip()
                    last_chapter_url = latest_chapter_tag['href']
                else:
                    last_chapter = "No chapter found"
                    last_chapter_url = "No chapter URL found"
            except Exception as e:
                print(f"Error parsing latest chapter: {e}")
                last_chapter = "No chapter found"
                last_chapter_url = "No chapter URL found"

            # Extract last chapter release date with dynamic class handling based on available data
            try:
                # Try finding the release date using the first class
                last_chapter_date_tag = details_soup.select_one("ul.row-content-chapter span.chapter-time.text-nowrap.fn-cover-item-time")
                
                # If the first class doesn't work, try the second class
                if not last_chapter_date_tag:
                    last_chapter_date_tag = details_soup.select_one("ul.row-content-chapter span.chapter-time.text-nowrap")

                if last_chapter_date_tag:
                    upload_date = last_chapter_date_tag.get('title', '').strip()
                    if upload_date:
                        # Convert to datetime object
                        last_chapter_release_date = datetime.strptime(upload_date, "%b %d,%Y %H:%M")
                    else:
                        last_chapter_release_date = None  # Default if no valid date found
                else:
                    last_chapter_release_date = None  # Default if tag not found
            except Exception as e:
                print(f"Error parsing last chapter release date: {e}")
                last_chapter_release_date = None  # Default if an error occurs


            # Return the populated Manga model
            return Manga(
                url=href,
                name=name,
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