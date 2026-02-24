FROM python:3.13-slim

WORKDIR /app

# 의존성 먼저 설치 (코드 변경 시 캐시 레이어 재활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 PDF 파일 복사
COPY app/ ./app/
COPY pdfs/ ./pdfs/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
