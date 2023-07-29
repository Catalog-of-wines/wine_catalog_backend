# wine/app/main.py
import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.staticfiles import StaticFiles

from app.auth.routes import router_auth
from app.comment.routes import router_comments
from app.product.routes import router_products
from app.users.routes import router_users

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://superb-malasada-e059fa.netlify.app",
    "https://dynamic-mermaid-e471dd.netlify.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_products)
app.include_router(router_auth)
app.include_router(router_comments)
app.include_router(router_users)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")


@app.get("/")
async def root():
    logger = logging.getLogger("uvicorn")
    logger.info("Received a request to root endpoint")
    return {
        "message": "This is root page Catalog of wine. "
                   "Use /docs endpoint to see API documentation"
    }


# delete this endpoint if it is not needed for front-end anymore
@app.get("/images/{image_path:path}", deprecated=True)
async def get_image(image_path: str):
    full_path = os.path.join(IMAGES_DIR, image_path)
    return FileResponse(full_path)
