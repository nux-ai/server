import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import asyncio


class AsyncWebScraper:
    def __init__(self, url: str, max_depth: int) -> None:
        self.url = self.format_url(url)
        self.max_depth = max_depth
        self.data = {
            "image": [],
            "video": [],
            "audio": [],
            "pdf": [],
            "html": [],
            "internal": [self.url],
        }

    @staticmethod
    def format_url(url: str) -> str:
        url = url.strip()
        if "http" not in url:
            url = f"http://{'www.' if 'www.' not in url else ''}{url}"
        return url

    async def scrape_data(self) -> dict:
        try:
            await self.recursive_scrape(0)
            return {
                "status": "ok",
                "message": "Scraping was successful.",
                "data": self.data,
            }, 200
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error during scraping: {str(e)}",
                "data": None,
            }, 500

    async def recursive_scrape(self, depth: int) -> None:
        if depth > self.max_depth:
            return
        print(f"Scraping level: {depth}")  # Print the current recursive level
        current_url = self.data["internal"][depth]
        page_content, status_code = await self.get_page_content(current_url)
        if status_code == 200:
            await self.process_page_content(current_url, page_content)
        await self.recursive_scrape(depth + 1)

    async def get_page_content(self, url: str) -> tuple:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                return BeautifulSoup(response.text, "html.parser"), 200
            except httpx.HTTPStatusError:
                return None, 400
            except Exception:
                return None, 500

    async def process_page_content(self, base_url: str, soup: BeautifulSoup) -> None:
        if soup:
            await self.extract_urls(soup, base_url)

    async def extract_urls(self, soup: BeautifulSoup, base_url: str) -> None:
        for tag in soup.find_all("a", href=True):
            href = self.clean_url(urljoin(base_url, tag["href"]))
            if self.is_valid_url(href) and href not in self.data["internal"]:
                self.categorize_url(href)

    @staticmethod
    def clean_url(url: str) -> str:
        parsed_url = urlparse(url)
        return f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)

    def categorize_url(self, url: str) -> None:
        if any(ext in url for ext in [".jpg", ".jpeg", ".png"]):
            self.data["image"].append(url)
        elif any(ext in url for ext in [".pdf"]):
            self.data["pdf"].append(url)
        elif any(ext in url for ext in [".html", ".htm"]):
            self.data["html"].append(url)
        elif url not in self.data["internal"]:
            self.data["internal"].append(url)
