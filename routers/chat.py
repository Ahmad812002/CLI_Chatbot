from pydantic import BaseModel
import openai
import os
from fastapi import APIRouter, HTTPException
from data_access.embeddings import get_embedding, search_embedding
from config.client import initialize_client
from config.prompts import chat_bot_prompt
from data_access.document_reader import add_embedding
from business_logic.llm import llm_chat

# Initialize the OpenAI client with the API key and base URL for OpenRouter.
client = initialize_client()

router = APIRouter()

class ChatRequest(BaseModel):
    message: str


# Handleing assistant mode.
@router.post("/chat")
def chat_bot(request: ChatRequest):
    try:
        reply = llm_chat(request.message)
        return {"ai_answer": reply}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:      
        raise HTTPException(status_code=500, detail=str(e))
