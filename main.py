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

# @app.get("/")
# def root():
#     return {"status": "running"}



# Handleing bot type (job_seeker or chat_bot)
def bot_mode():
    print("Welcome to the AI Career Coach!")
    print("Please select a mode:")
    print("\n1. Assistant\n")
    print("2. Job Seeker")

    while True:
        mode = input("Enter the number of your choice (or type 'exit' to quit): ").strip().lower()
        if mode in ["1", "assistant"]:
            chat.chat_bot_mode()
            break
        elif mode in ["2", "job seeker", "job_seeker"]:
            scorer.scorer_endpoint()
            break
        elif mode in ["exit", "quit"]:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    try:
        bot_mode()
    except KeyboardInterrupt:
        print("\nSession ended.")



# routers
# @app.get("/chat_bot")
# def chat_bot_endpoint():
#     chat_bot_mode()

# # def job_scorer_endpoint():
# #     job_scorer_mode()
# @app.post("/preferences")
# def update_preferences_endpoint():
#     try:
#         update_preferences()
#         return {"status": "success", "message": "Preferences updated successfully."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# @app.get("/preferences")
# def get_preferences_endpoint():
#     try:
#         preferences = get_preferences_collection()
#         if preferences is not None:
#             return {"status": "success", "preferences": preferences}
#         else:
#             return {"status": "error", "message": "No preferences found."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

# #must take a file path (drag and drop)
# @app.post("/ingest_document")
# def ingest_document_endpoint(file_path: str):
#     try:
#         add_embedding(file_path)
#         return {"status": "success", "message": "Document ingested successfully."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}


app.include_router(scorer.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(cover_letter.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(preferences.router, prefix="/api/v1")


if __name__ == "__main__":
    main()