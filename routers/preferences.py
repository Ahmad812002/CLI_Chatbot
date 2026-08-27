from anthropic import BaseModel
import requests
from typing import Optional
from fastapi import APIRouter
from data_access.db import get_preferences_collection
import json

router = APIRouter()

ids = get_preferences_collection().get()["ids"]

class PreferencesRequest(BaseModel):
    preferences: Optional [str]

@router.post("/update_preferences")
# Update preferenes
def update_preferences(request: PreferencesRequest):
    global ids
    doc_id = str(max(int(i) for i in ids) + 1)

    try:
        existing_preferences = get_preferences_collection()
        if existing_preferences is not None:
            print("Preferences already exist in the database, if you wanna update them now write 'update'.")
            update_choice = input("You: ").strip().lower()
            if update_choice == "update":
                print("Which preferences you are looking for in your next job? (e.g. remote, hybrid, full-time, part-time, contract, internship, location etc.)")
                preferences_input = input("You: ").strip()
                try:
                    get_preferences_collection().update(
                        ids=[str(int(0))],
                        documents=[preferences_input],
                    )
                    return get_preferences_collection().get()
                except Exception as e:
                    print(f"Error occurred while updating preferences: {e}")
                    return
            return existing_preferences
    except Exception as e:
        print(f"Error occurred while checking preferences: {e}")
        return

@router.post("/add_preferences")
def add_preferences(request: PreferencesRequest):
    global ids
    doc_id = str(max(int(i) for i in ids) + 1)
    
    try:
        get_preferences_collection().add(
        ids=doc_id,
        documents=[request.preferences],
        )
        return {"status": "successfully"}
    except Exception as e:
        print(f"Error occurred while adding preferences: {e}")
        return

