from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import httpx
from src.researcher.services.insta_persona_service import InstaPersonaService
from src.researcher.language_models.openai_client import OpenAIClient
from src.researcher.services.story_creation_service import StoryCreationService

load_dotenv()

router = APIRouter()

class CodeRequest(BaseModel):
    code: str
    source: str = "local"

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

class ChatRequest(BaseModel):
    user_message: str
    user_id: str

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

@router.post("/get-user-fb")
async def gather_data(request: CodeRequest):
    
    if request.source == "local":
        response = {"status": "received code", "source": "local"}
        return response
    else:
        response = {"status": "received code", "source": "external"}
                
@router.get("/user_object_graph")
async def user_object_graph():
    service = InstaPersonaService()
    try:
        result = await service.fetch_user_media_urls()
        graph_json = await service.get_profile_object_graph(result[0:10])
        return {"graph": graph_json}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chat")
async def chat(request: ChatRequest):
    service = OpenAIClient()
    try:
        result = await service.chat(request.user_id, request.user_message, "You are a friendly and insightful character chatbot.")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat-persona")
async def chat(request: ChatRequest):
    service = InstaPersonaService()
    try:
        result = await service.chat_with_character(request.user_id, request.user_message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat-timeline")
async def chat(request: ChatRequest):
    service = InstaPersonaService()
    try:
        result = await service.chat_with_timeline_builder(request.user_id, request.user_message)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat-history/{user_id}")
async def chat_history(user_id: str):
    service = OpenAIClient()
    try:
        result = await service.read_user_chat_history(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user-timeline/{user_id}")
async def user_timeline(user_id: str):
    service = StoryCreationService()
    try:
        result = await service.fetch_user_story(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))