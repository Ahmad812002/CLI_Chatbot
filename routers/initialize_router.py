
from fastapi import APIRouter, HTTPException


try: router = APIRouter()
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error occurred while initializing router: {str(e)}")