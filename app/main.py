import uvicorn
from app.config import api_cfg, LOGGING_CONFIG, agent_cfg
from fastapi import FastAPI
from app.api import agents

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Growth Agent API"}


app.include_router(agents.router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=api_cfg.HOST,
        port=api_cfg.PORT,
        reload=True,
        log_config=LOGGING_CONFIG,
    )
