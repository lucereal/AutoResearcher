from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controller.researcher_controller import router as researcher_router
from controller.insta_user_controller import router as insta_user_router
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import Config, Server
import asyncio


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "https://localhost:3000",  # Add your frontend URL here
    # Add other allowed origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(researcher_router, prefix="/researcher")
app.include_router(insta_user_router, prefix="/insta-user")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
class ProactorServer(Server):
    def run(self, sockets=None):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop) # since this is the default in Python 3.10, explicit selection can also be omitted
        asyncio.run(self.serve(sockets=sockets))

if __name__ == '__main__':
    config = Config(app=app, host="0.0.0.0", port=8000, reload=True)
    server = ProactorServer(config=config)
    server.run()