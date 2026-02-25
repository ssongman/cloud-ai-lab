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


if __name__ == "__main__":
    import sys
    import os
    # 프로젝트 루트를 sys.path에 추가 (play 버튼 실행 시 app/ 디렉토리가 기준이 되는 문제 해결)
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
