from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.researcher.agents.data_gatherer import DataGatherer
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Add your frontend URL here
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the DataGatherer service
data_gatherer = DataGatherer()

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

@app.post("/gather_data")
def gather_data(request: TopicRequest):
    if request.source in ["news", "youtube"]:
        raise HTTPException(status_code=400, detail=f"The source '{request.source}' is not implemented.")
    
    user_topic = request.topic
    if request.source == "default_source":
        result = data_gatherer.gather_newsapi_data_and_summarize_sources(user_topic)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown source: {request.source}")
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)