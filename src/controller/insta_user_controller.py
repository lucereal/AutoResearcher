from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx

load_dotenv()

router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    source: str = "local"

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

@router.post("/get-user")
async def gather_data(request: CodeRequest):
    client_id = os.getenv("INSTAGRAM_CLIENT_ID")
    client_secret = os.getenv("INSTAGRAM_CLIENT_SECRET")
    grant_type = "authorization_code"
    redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")
    code = request.code
    a_code = os.getenv("INSTAGRAM_ACCESS_CODE")

    url = "https://api.instagram.com/oauth/access_token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "redirect_uri": redirect_uri,
        "code": code
        }
    
    if request.source == "local":
        response = {"access_token": a_code}
        return response
    else:
        async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise HTTPException(status_code=response.status_code, detail=response.text)
