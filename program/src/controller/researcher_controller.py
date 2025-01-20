from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.researcher.agents.data_gatherer import DataGatherer
from src.researcher.agents.newsapi_agent import NewsApiAgent



router = APIRouter()

# Initialize the DataGatherer service
data_gatherer = DataGatherer()

newsapi_agent = NewsApiAgent()

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

@router.post("/gather_data")
async def gather_data(request: TopicRequest):
    if request.source in ["news", "youtube"]:
        raise HTTPException(status_code=400, detail=f"The source '{request.source}' is not implemented.")
    
    user_topic = request.topic
    if request.source == "default_source":
        #result = await data_gatherer.gather_newsapi_data_and_summarize_sources(user_topic)
        result = await newsapi_agent.gather_topic_summarization(user_topic, 1, 5)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown source: {request.source}")
    
    return result





