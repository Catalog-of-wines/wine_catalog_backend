# # run.py
#
# import uvicorn
# import os
#
# from fastapi import APIRouter, FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from starlette.staticfiles import StaticFiles
#
#
# app = FastAPI()
# router = APIRouter()
#
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://localhost:3000",
#     "https://superb-malasada-e059fa.netlify.app",
#     "https://64b79ef90dd1ff62287a5770--peppy-seahorse-d9c071.netlify.app/",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# app.include_router(router)
#
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# IMAGES_DIR = os.path.join(BASE_DIR, "images")
# app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")
#
#
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
