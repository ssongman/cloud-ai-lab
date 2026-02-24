import sys
import os

# play 버튼으로 직접 실행 시 프로젝트 루트를 sys.path에 추가 (imports 이전에 실행되어야 함)
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from contextlib import asynccontextmanager  # noqa: E402

from fastapi import FastAPI  # noqa: E402

from app.routers import chat, admin  # noqa: E402
from app.services.vector_store import build_index  # noqa: E402


@asynccontextmanager
async def lifespan(_app: FastAPI):
    build_index()
    yield


app = FastAPI(title="KnowledgeOps API", lifespan=lifespan)

app.include_router(admin.router, prefix="/knowledgeops/api")
app.include_router(chat.router, prefix="/knowledgeops/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
