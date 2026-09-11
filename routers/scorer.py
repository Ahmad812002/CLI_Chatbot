from pydantic import BaseModel
from data_access.db import get_embeddings_collection, get_preferences_collection
from config.client import initialize_client
from fastapi import APIRouter, HTTPException
from business_logic.scorer_logic import run_scorer


router = APIRouter()

ids = get_embeddings_collection().get()["ids"]

client = initialize_client()


messages_arr = []
last_reply = ""

# This class to make a clear response from FastAPI
class ScoreRequest(BaseModel):
    job_description: str


@router.post('/scorer')
def scorer_endpoint(request: ScoreRequest):
    try:
        # now it gets directly from database, the UI should ask for them if there is nothing stored
        preferences = get_preferences_collection().get()["documents"]

        result = run_scorer(request.job_description, preferences)
        return result
    except ValueError as e:
        raise  HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

