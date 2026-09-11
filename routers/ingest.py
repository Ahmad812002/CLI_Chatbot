from fastapi.responses import JSONResponse
from pydantic import BaseModel 
from fastapi import APIRouter, HTTPException
from data_access.document_reader import add_embedding
from data_access.db import get_embeddings_collection

router = APIRouter()

class IngestRequest(BaseModel):
    file_path: str

@router.post("/ingest_document")
def ingest_document(request: IngestRequest):
    try:
        # Get the current maximum ID from the embeddings collection and increment it for the new document
        ids = get_embeddings_collection().get()["ids"]
        doc_id = str(max(int(i) for i in ids) + 1)
        return add_embedding(request.file_path, doc_id)
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while ingesting document: {str(e)}")