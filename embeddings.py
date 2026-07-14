from nomic import embed
import numpy as np
import chromadb
from dotenv import load_dotenv
import os
import fitz
import docx
import PyPDF2

load_dotenv()

#try:       
    #chroma_client = chromadb.CloudClient(
        #database details
    #)
    #collection = chroma_client.get_collection(name="")
#except Exception as e:
    #print(f"Error occurred while connecting to ChromaDB: {e}")


# query_vector = get_embedding(user_input)
# Then you compare this query vector against every stored document vector and rank by similarity score

def read_document(document):
    try:
        # Plain string passed directly.
        if not document.endswith(('.pdf', '.txt', '.docx', '.md')):
            return document.strip()  # If it's not a file, treat it as raw text and return it.
        # Text-based documents, read the content and return it as a string.
        if document.endswith(('.txt', '.md')):
            try:
                with open(document, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            except Exception as e:
                print(f"Error occurred while reading text document: {e}")
        # PDF documents
        if(document.endswith('.pdf')):
            text = ""
            try:
                with open(document, 'rb') as f:
                    read_pdf = PyPDF2.PdfReader(document)
                    for i in range(len(read_pdf.pages)):
                        page = read_pdf.pages[i]
                        text += page.extract_text()
                return text.strip()   
            except Exception as e:
                print(f"Error occurred while reading PDF document: {e}")
        # Word docuements
        if(document.endswith('.docx')):
            try:
                doc = docx.Document(document)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text.strip()
            except Exception as e:
                print(f"Error occurred while reading Word document: {e}")
    except FileNotFoundError:
        print(f"File not found: {document}")
        return None
    except Exception as e:
        print(f"Error occurred while reading document: {e}")
        return None

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
        collection.add(
            ids = [doc_id],
            documents = [text],
            embeddings = [embedding],
            metadatas = [{"source": source}]
        )
        print("Embedding stored successfully.")
        return True
    except Exception as e:
        print(f"Error occurred while storing embedding: {e}")
        return False
# This function is to search the embedding in ChromaDB, it will take the query vector as input and return the top 3 closest documents.
def search_embedding(query_vector):
    try:
        results = collection.query(
                query_embeddings=[query_vector],
                n_results=3
            )
    except Exception as e:
        print(f"Error occurred while searching embedding: {e}")
        return None

    # Threshold filtering by similarity score (e.g., 0.8)
    threshold = 0.7
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

