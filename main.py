from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
# from data_access.db import get_preferences_collection
from routers import scorer, chat, cover_letter, preferences, ingest
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()
router = APIRouter()

origins = [
    "http://localhost",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "*"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

# def main():
#     try:
#         app.include_router(scorer.router, prefix="/api/v1", tags=["scorer"])
#         app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
#         app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
#         app.include_router(cover_letter.router, prefix="/api/v1", tags=["cover-letter"])
#         app.include_router(preferences.router, prefix="/api/v1", tags=["preferences"])
#     except Exception as e:
#         print("Session ended.", e)


app.include_router(scorer.router, prefix="/api/v1", tags=["scorer"])
app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
app.include_router(ingest.router, prefix="/api/v1", tags=["ingest"])
app.include_router(cover_letter.router, prefix="/api/v1", tags=["cover-letter"])
app.include_router(preferences.router, prefix="/api/v1", tags=["preferences"])


if __name__ == "__main__":
    main()