from anthropic import BaseModel
from data_access.embeddings import get_embedding, search_embedding
from data_access.db import get_embeddings_collection, get_preferences_collection
from config.client import initialize_client
import openai
from config.prompts import job_scorer_prompt
from fastapi import APIRouter
from business_logic.llm import llm_scorer


ids = get_embeddings_collection().get()["ids"]

client = initialize_client()

router = APIRouter()

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
        print("\n\n\n", result)
    except Exception as e:
        return {"error": e}
    return result

def run_scorer(job_description: str, job_preferences: str):
    try:
        
        # validate
        if len(job_description.strip()) < 50:
            return {"error": "Please provide a valid job description"}
        
        # process
        profile_chunks = process_job_description(job_description)
        formatted_prompt = job_scorer_prompt(profile_chunks, job_preferences, job_description)
        llm_answer = llm_scorer(formatted_prompt)
        
        if llm_answer is None:
            return {"error": "Could not generate a response"}
    except Exception as e:
        return {
            "error": e
        }
    
    # return
    return {
        "result": llm_answer,
        "profile_chunks": profile_chunks,
        "job_description": job_description
    }

# def llm_scorer(prompt):
#     try:
#         response = client.chat.completions.create(
#         model="gpt-oss-120b",
#         messages= [prompt] + messages_arr[-10:] ,
#         max_tokens=1024,
#         temperature=0.0 # For a job fit scorer, reliable scoring, temperature (creativity) should be low
#     )
#     except openai.APIError as e:
#         return{ "API Error: ": e }
#     except openai.APITimeoutError as e:
#         return { "Timeout Error: ": e }
#     except openai.APIConnectionError as e:
#         return { "API Connection Error: ": e }
#     except openai.BadRequestError as e:
#         return { "Invalid Request Error (Bad Request): ": e }
#     except openai.InternalServerError as e:
#         return { "Internal Server Error: ": e }
#     except openai.RateLimitError as e:
#         return{ "Rate Limit Error: ": e }
#     except openai.AuthenticationError as e:
#         return { "Authentication Error: ": e }

#     return response.choices[0].message.content

# It will get the embedding of the entire job description and search for similar documents in the database.
def process_job_description(job_description):
    try:
        job_embedding = get_embedding(job_description)
        profile_chunks = search_embedding(job_embedding)
        if profile_chunks:
            return "\n".join([chunk['documents'] for chunk in profile_chunks])
        return None
    except Exception as e:
        print(f"Error occurred while processing job description: {e}")
        return None
