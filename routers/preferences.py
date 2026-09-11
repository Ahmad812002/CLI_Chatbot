from pydantic import BaseModel 
import requests
from typing import Optional
from fastapi import APIRouter, HTTPException
from data_access.db import get_preferences_collection
import json

router = APIRouter()

PREFERENCES_ID = "user_preferences"

class PreferencesRequest(BaseModel):
    preferences: Optional [str]

@router.post("/add_preferences")
# Add or update user preferences in the database.
def update_preferences(request: PreferencesRequest):
    try:
        get_preferences_collection().upsert(
            ids=[PREFERENCES_ID],
            documents=[request.preferences],
        )
        return get_preferences_collection().get()
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(status_code=404, detail="No preferences found. Please set preferences first.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

