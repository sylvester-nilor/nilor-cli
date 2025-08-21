import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent_service import AgentService

app = FastAPI(title="Knowledge Agent", version="1.0.0")


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def health_check():
    return {"status": "healthy", "service": "knowledge-agent"}


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    try:
        project_id = os.getenv("GCP_PROJECT", "robot-rnd-nilor-gcp")
        book_agent_url = os.getenv("BOOK_AGENT_URL", "https://book-agent-v1-959508709789.us-central1.run.app")
        auth_token = os.getenv("AUTH_TOKEN")

        service = AgentService(
            project_id=project_id,
            book_agent_url=book_agent_url,
            auth_token=auth_token
        )

        response = service.chat(
            message=request.message,
            thread_id=request.thread_id
        )

        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
