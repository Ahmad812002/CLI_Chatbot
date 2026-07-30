from nomic import embed
import numpy as np
from dotenv import load_dotenv
from data_access.db import embeddings_collection

load_dotenv()
    


# This function is to chunk the text into smaller pieces,
#  it will take the text as input and return a list of chunks.
def chunk_text(text):
    # This function applies a simple chunking strategy based on a fixed character limit.
    chunk_size = 500
    overlap_size = 50
    chunks = []
    try:
        for i in range(0, len(text), chunk_size - overlap_size): # Move back by overlap_size to create overlap
            chunks.append(text[i:i+chunk_size])
    except Exception as e:
        print(f"Error occurred while chunking text: {e}")
    return chunks 

# This function is to get the embedding of a given text, it will return the embedding vector.
def get_embedding(text):
    try:
        response = embed.text(
            texts=[text],
            model="nomic-embed-text-v1.5",
            task_type="search_document",
        )
        embeddings = np.array(response['embeddings'][0])
        return embeddings
    except Exception as e:
        print(f"Error occurred while generating embedding: {e}")
        return None
# This function is to store the embedding in ChromaDB, it will take the document id, text and embedding vector as input and store it in the collection.
def store_embedding(doc_id, text, embedding, source):
    
    try:
        embeddings_collection.add(
            ids = [doc_id],
            documents = [text],
            embeddings = [embedding],
            metadatas = [{"source": source}]
        )
        print("Document ingested successfully!")
        return True
    except Exception as e:
        print(f"Error occurred while storing embedding: {e}")
        return False
# This function is to search the embedding in ChromaDB, it will take the query vector as input and return the top 3 closest documents.
def search_embedding(query_vector):
    try:
        results = embeddings_collection.query(
                query_embeddings=[query_vector],
                n_results=10

            )
    except Exception as e:
        print(f"Error occurred while searching embedding: {e}")
        return None

    # Threshold filtering by similarity score (e.g., 0.7)
    threshold = 0.6
    chunks = []
    try: 
        for index, distance in enumerate(results['distances'][0]):
            # How far are they from each other? (lower is closer)
            print(results['distances'][0][index])
            if(distance <= threshold):
                # Convert passing chunks into a list
                chunks.append({
                    'distances': distance,
                    'documents': results['documents'][0][index],
                    'metadata': results['metadatas'][0][index]
                })
            else:
                pass
    except Exception as e:
        print(f"Error occurred while processing search results: {e}")
    if chunks == None:
        print("There is no similar document found in the database.")
        return None
    else:
        print(f"Found {len(chunks)} similar documents in the database.")
        print(f"Chunks: {chunks}")
        return chunks

