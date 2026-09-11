import docx
import PyPDF2
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from data_access.embeddings import chunk_text, store_embedding, get_embedding
from data_access.db import get_embeddings_collection


# reading four types of ducments 
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
                raise HTTPException(status_code=500, detail=f"Error occurred while reading text document: {str(e)}")
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
                raise HTTPException(status_code=500, detail=f"Error occurred while reading PDF document: {str(e)}")
        # Word docuements
        if(document.endswith('.docx')):
            try:
                doc = docx.Document(document)
                text = "\n".join([para.text for para in doc.paragraphs])
                return text.strip()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error occurred while reading Word document: {str(e)}")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"File not found: {document}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while reading document: {str(e)}")

# Handleing document, chunk it into smaller pieces, get the embedding of each chunk and store the embedding in the database.
def add_embedding(user_input, doc_id):
    try:
        document = read_document(user_input)
        text_chunks = chunk_text(document)
        
        
        ids = get_embeddings_collection().get()["ids"]

        doc_id = str(max(int(i) for i in ids) + 1)

        for chunk in text_chunks:
            if(len(chunk.strip()) < 100):  # Skip chunks that are too short
                    continue
            embedding = get_embedding(chunk)
            store_embedding(doc_id, chunk, embedding, source=user_input)
            doc_id = str(int(doc_id) + 1)
        return JSONResponse(status_code=201, content={"message": "Document ingested successfully"})
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail={f"File not found: {user_input}"})
    except ValueError as e:
        raise HTTPException(status_code=400, detail={f"Value error: {str(e)}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail={f"Server error occurred while processing the document: {str(e)}"})
