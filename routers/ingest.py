from anthropic import BaseModel
from fastapi import APIRouter
from data_access.document_reader import add_embedding
from data_access.db import get_embeddings_collection

router = APIRouter()

class IngestRequest(BaseModel):
    file_path: str

@router.post("/ingest_document")
def ingest_document(request: IngestRequest):
    ids = get_embeddings_collection().get()["ids"]
    doc_id = str(max(int(i) for i in ids) + 1)
    return add_embedding(file_path, doc_id)