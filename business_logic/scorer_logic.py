from fastapi import HTTPException

from data_access.embeddings import get_embedding, search_embedding
from config.prompts import job_scorer_prompt
from business_logic.llm import llm_scorer
import json

def run_scorer(job_description: str, job_preferences: str):
    try:
        # validate
        if len(job_description.strip()) < 50:
            raise HTTPException(status_code=400, detail="Job description too short")
        
        # process
        profile_chunks = process_job_description(job_description)
        if(profile_chunks is None):
            return None
        
        formatted_prompt = job_scorer_prompt(profile_chunks, job_preferences, job_description)
        raw_result = llm_scorer(formatted_prompt)

        if(raw_result is None or raw_result.strip() == ""):
            raise HTTPException(status_code=500, detail="LLM returned no response")

        parsed = format_scorer_result_json(raw_result)
        if(parsed is None):
            raise HTTPException(status_code=500, detail="LLM returned no response")
        return {
            "matching_points": parsed['matching_points'],
            "gaps": parsed['gaps'],
            "reasoning": parsed['reasoning'],
            "profile_chunks": profile_chunks,
            "job_description": job_description
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error occurred while running scorer: {str(e)}")

    

# It will get the embedding of the entire job description and search for similar documents in the database.
def process_job_description(job_description):
    try:
        job_embedding = get_embedding(job_description)
        profile_chunks = search_embedding(job_embedding)
        if profile_chunks:
            return "\n".join([chunk['documents'] for chunk in profile_chunks])
        return None
    except Exception as e:
        raise ValueError(status_code=500, detail=f"Error occurred while processing job description: {str(e)}")


def format_scorer_result_json(ai_reply):
    try:
        result = json.loads(ai_reply)
        return {
            "matching_points": result['matching_points'],
            "gaps": result['gaps'],
            "reasoning": result['reasoning']
        }
    except json.JSONDecodeError:
        raise ValueError(status_code=500, detail=f"LLM returned invalid JSON: {ai_reply[:10]}")
       
