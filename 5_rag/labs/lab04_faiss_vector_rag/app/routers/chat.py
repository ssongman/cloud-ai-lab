from fastapi import APIRouter, HTTPException
from langchain_community.callbacks import get_openai_callback

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.vector_store import get_vectorstore
from app.services.rag import rag_chain
from app.config import SEARCH_TOP_K

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    vectorstore = get_vectorstore()
    if vectorstore is None:
        raise HTTPException(status_code=503, detail="벡터 인덱스가 초기화되지 않았습니다.")

    retrieved_docs = vectorstore.similarity_search(request.question, k=SEARCH_TOP_K)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    with get_openai_callback() as cb:
        answer = rag_chain.invoke({"context": context, "question": request.question})

    return ChatResponse(
        answer=answer,
        tokens=cb.total_tokens,
        prompt_tokens=cb.prompt_tokens,
        completion_tokens=cb.completion_tokens,
        cost=cb.total_cost,
    )
