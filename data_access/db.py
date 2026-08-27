import chromadb
import os



try:       
    chroma_client = chromadb.CloudClient(
        tenant='f4693080-0a9c-4c15-b7b0-8596835296b3',
        database='ahmad_database',
        api_key=os.getenv('CHROMA_API_KEY')
    )
except Exception as e:
    print(f"Error occurred while connecting to ChromaDB: {e}")

def get_preferences_collection():
    try:
        return chroma_client.get_collection(name="preferences")
    except Exception as e:
        print(f"Error occurred while retrieving preferences records: {e}")
        return None


def update_preferences_record(record_id, new_preferences):
    try:
        get_preferences_collection().update(
            ids=[record_id],
            documents=[new_preferences]
        )
    except Exception as e:
        print(f"Error occurred while updating preferences record: {e}")


def get_embeddings_collection():
    try:
        return chroma_client.get_collection(name="embeddings")
    except Exception as e:
        print(f"Error occurred while retrieving document records: {e}")
        return None

