from http.client import HTTPException

import chromadb
import os



try:       
    chroma_client = chromadb.CloudClient(
        tenant='f4693080-0a9c-4c15-b7b0-8596835296b3',
        database='ahmad_database',
        api_key=os.getenv('CHROMA_API_KEY')
    )
except Exception as e:
    raise HTTPException(status_code=500, detail="Database connection failed")

def get_preferences_collection():
    try:
        return chroma_client.get_collection(name="preferences")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error occurred while retrieving preferences records: {str(e)}")


def update_preferences_record(record_id, new_preferences):
    try:
        get_preferences_collection().update(
            ids=[record_id],
            documents=[new_preferences]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error occurred while updating preferences record: {str(e)}")


def get_embeddings_collection():
    try:
        return chroma_client.get_collection(name="embeddings")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error occurred while retrieving document records: {str(e)}")

