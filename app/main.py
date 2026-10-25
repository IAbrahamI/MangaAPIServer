import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.src.scripts.service_handler import ServiceHandler

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
service_handler = ServiceHandler()

SCRAPE_INTERVAL_SECONDS = 3 * 60 * 60


async def scheduled_scrape():
    """Scrape all mangas at startup and then every SCRAPE_INTERVAL_SECONDS."""
    while True:
        try:
            await asyncio.to_thread(service_handler.update_all_entries, "schedule")
        except Exception:
            logger.exception("Scheduled scrape failed")
        await asyncio.sleep(SCRAPE_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(scheduled_scrape())
    yield
    task.cancel()


app = FastAPI(
    title="My Mangas API",
    description="API for all my favourite mangas created to be callable through an API",
    version="1.0.0",
    docs_url="/docs",  # Enable /docs for Swagger UI
    redoc_url=None,    # Disable /redoc (optional)
    lifespan=lifespan
)
origins = [
    "http://localhost",
    "http://192.x.x.x",
    "http://*:80",
    "http://*:8000",
    "http://*:443",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Disable the default root route
@app.get("/", include_in_schema=False)
def root():
    return JSONResponse(status_code=404, content={"message": "API Only"})

@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}

@app.get("/mangas")
def get_mangas():
    return service_handler.get_all_entries()


@app.get("/mangas/{manga_name}")
def get_manga(manga_name: str):
    return service_handler.retrieve_manga(manga_name)


@app.post("/mangas/{manga_name}")
def add_manga(manga_name: str):
    return service_handler.create_entry(manga_name)

@app.delete("/mangas/{manga_name}")
def remove_manga(manga_name: str):
    return service_handler.remove_manga(manga_name)

@app.put("/mangas")
def update_mangas():
    return service_handler.update_all_entries("manual")
