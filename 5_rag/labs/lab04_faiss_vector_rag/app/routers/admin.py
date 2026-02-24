from fastapi import APIRouter, HTTPException

from app.services.vector_store import build_index, get_vectorstore, get_pdf_files
from app.config import PDF_DIR

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok",
        "index_loaded": get_vectorstore() is not None,
        "pdf_dir": str(PDF_DIR),
        "pdfs": [f.name for f in get_pdf_files()],
    }


@router.post("/index/rebuild")
async def rebuild_index():
    pdf_files = get_pdf_files()
    if not pdf_files:
        raise HTTPException(status_code=404, detail=f"PDF 파일이 없습니다: {PDF_DIR}")
    result = build_index(force=True)
    return {"message": "벡터 인덱스가 재생성되었습니다.", **result}
