from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uvicorn import Config, Server
from src.researcher.agents.data_gatherer import DataGatherer
from src.researcher.agents.newsapi_agent import NewsApiAgent
import json
import os
import asyncio

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

newsapi_agent = NewsApiAgent()

class TopicRequest(BaseModel):
    topic: str
    source: str = "default_source"

@app.post("/gather_data")
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


class ProactorServer(Server):
    def run(self, sockets=None):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop) # since this is the default in Python 3.10, explicit selection can also be omitted
        asyncio.run(self.serve(sockets=sockets))

if __name__ == '__main__':
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)
    server = ProactorServer(config=config)
    server.run()




# if __name__ == "__main__":
#     if os.name == "nt":
#         loop = asyncio.ProactorEventLoop()
#         asyncio.set_event_loop(loop)
#         # asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
#     #     uvicorn.run(
#     #     "test:app",
#     #     host="0.0.0.0",
#     #     reload=False,
#     #     port=8002
#     # )