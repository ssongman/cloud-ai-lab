import os
import shutil
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader

from app.config import PDF_DIR, FAISS_INDEX_PATH

embeddings = OpenAIEmbeddings()
_vectorstore: FAISS | None = None


def get_vectorstore() -> FAISS | None:
    return _vectorstore


def get_pdf_files() -> list[Path]:
    """pdfs/ 디렉토리의 PDF 파일 목록을 반환한다."""
    return sorted(PDF_DIR.glob("*.pdf"))


def build_index(force: bool = False) -> dict:
    global _vectorstore

    if not force and os.path.exists(FAISS_INDEX_PATH):
        print("📂 저장된 벡터 인덱스를 로드합니다.")
        _vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )
        return {"action": "loaded", "path": FAISS_INDEX_PATH}

    pdf_files = get_pdf_files()
    if not pdf_files:
        raise FileNotFoundError(f"PDF 파일이 없습니다: {PDF_DIR}")

    print("🔄 PDF를 로드하고 벡터 인덱스를 새로 생성합니다.")
    if os.path.exists(FAISS_INDEX_PATH):
        shutil.rmtree(FAISS_INDEX_PATH)

    all_documents = []
    for pdf_path in pdf_files:
        print(f"  📄 로드 중: {pdf_path.name}")
        loader = PyPDFLoader(str(pdf_path))
        all_documents.extend(loader.load_and_split())

    print(f"📄 총 청크 수: {len(all_documents)} (PDF {len(pdf_files)}개)")
    _vectorstore = FAISS.from_documents(documents=all_documents, embedding=embeddings)
    _vectorstore.save_local(FAISS_INDEX_PATH)
    print("💾 벡터 인덱스를 저장했습니다.")

    return {
        "action": "created",
        "pdf_count": len(pdf_files),
        "pdfs": [f.name for f in pdf_files],
        "total_chunks": len(all_documents),
        "path": FAISS_INDEX_PATH,
    }
