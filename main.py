from fastapi import FastAPI
from api.messages import router as messages_router
from api.sessions import router as sessions_router
from api.rag import router as rag_router

app = FastAPI(title="Oncall Agent")
app.include_router(sessions_router)
app.include_router(rag_router)
app.include_router(messages_router)
@app.get("/")
def read_root():
    return{"message":"Hello World"}


@app.get("/health")
def health_check():
    return{"status":"ok"}

#& "C:\Users\30521\Desktop\oncall-agent\start-dev.ps1"





