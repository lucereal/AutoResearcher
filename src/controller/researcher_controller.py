from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.researcher.agents.data_gatherer import DataGatherer

app = FastAPI()

# Initialize the DataGatherer service
data_gatherer = DataGatherer()

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

@app.post("/gather_data")
async def gather_data(request: TopicRequest):
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