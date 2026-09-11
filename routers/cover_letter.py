from unittest import result

from pydantic import BaseModel 
from business_logic.cover_letter_logic import run_cover_letter 
from fastapi import APIRouter, HTTPException
from business_logic.scorer_logic import process_job_description, run_scorer
from data_access.db import get_preferences_collection

router = APIRouter()

class CoverLetterRequest(BaseModel):
    job_description: str
    profile_chunks: str = ""
    matching_points: list[str] = []
    gaps: list[str] = []
    reasoning: str = ""
    

@router.post("/cover_letter")
def generate_cover_letter(request: CoverLetterRequest):
    try:
        job_preferences = get_preferences_collection().get()["documents"]
        scorer_result = run_scorer(request.job_description, job_preferences)
        profile_chunks = process_job_description(request.job_description)

        generated_cover_letter = run_cover_letter(profile_chunks,
                                                request.job_description,
                                                scorer_result['matching_points'],
                                                scorer_result['gaps'], 
                                                scorer_result['reasoning'])

        if(generated_cover_letter['opening']):
            return {
                        "opening": generated_cover_letter['opening'],
                        "middle": generated_cover_letter['middle'],
                        "gap": generated_cover_letter['gap'],
                        "closing": generated_cover_letter['closing']
                        }
    except ValueError as e:
        raise  HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
