from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# 프로젝트 루트 기준 절대 경로로 지정 (uvicorn 실행 위치와 무관하게 동작)
BASE_DIR = Path(__file__).parent.parent

PDF_DIR = BASE_DIR / "pdfs"          # PDF 파일을 이 디렉토리에 넣으면 자동 인덱싱
FAISS_INDEX_PATH = str(BASE_DIR / "faiss_index")

OPENAI_MODEL = "gpt-3.5-turbo"
SEARCH_TOP_K = 3
