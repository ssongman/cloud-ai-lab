from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import chat, admin
from app.services.vector_store import build_index


@asynccontextmanager
async def lifespan(_app: FastAPI):
    build_index()
    yield


app = FastAPI(title="KnowledgeOps API", lifespan=lifespan)

app.include_router(admin.router, prefix="/knowledgeops/api")
app.include_router(chat.router, prefix="/knowledgeops/api")
