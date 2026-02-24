

# 1. 구조



```sh

lab04_faiss_vector_rag/
├── main.py                      ← uvicorn 진입점 (1줄)
├── app/
│   ├── main.py                  ← FastAPI 앱 생성 + lifespan + 라우터 등록
│   ├── config.py                ← PDF 경로, 모델명 등 설정값
│   ├── schemas/
│   │   └── chat.py              ← ChatRequest / ChatResponse 모델
│   ├── services/
│   │   ├── vector_store.py      ← FAISS 인덱스 빌드/로드
│   │   └── rag.py               ← LLM + 프롬프트 + RAG 체인
│   └── routers/
│       ├── chat.py              ← POST /knowledgeops/api/chat
│       └── admin.py             ← GET /health, POST /index/rebuild



lab04_faiss_vector_rag/
├── pdfs/                                    ← PDF 보관 디렉토리
│   ├── 25년의용소방대결산.pdf
│   └── 의용소방대_척사대회찬조품.pdf



```

- **config** - 설정 변경은 이 파일 하나만 수정하면 됨
- **services** - 비즈니스 로직 (FAISS, LLM)
- **routers** - HTTP 요청/응답 처리
- **schemas** - 데이터 구조 정의





# 2. 실행



## 1) 서버 기동 방법



```bash

$ python3 -m venv venv

$ source venv/bin/activate

$ uvicorn app.main:app --host 0.0.0.0 --port 8000


$ deactivate


```

**앱 동작 방식**

- 서버 시작 시 `lifespan`이 `build_index()`를 자동 호출
- `faiss_index` 폴더가 있으면 기존 인덱스 로드, 없으면 PDF로 새 인덱스 생성
- `/index/rebuild` 호출 시 기존 인덱스 삭제 후 PDF에서 강제 재생성



### 서버 중지시

```sh

lsof -ti :8000 -ti :8001 2>/dev/null


lsof -ti :8000 -ti :8001 | xargs kill -9 2>/dev/null && echo "종료 완료"


```



## 2) API



### (1) health

```sh

$ curl http://localhost:8000/knowledgeops/api/health -i

```



### (2) chat 요청/응답 예시

```bash
# 요청
$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "고체연료로 지출한 금액이 얼마야?"}'

# 응답
{
  "answer": "고체연료로 지출한 금액은 45,000원이다.",
  "tokens": 614,
  "prompt_tokens": 592,
  "completion_tokens": 22,
  "cost": 0.000329
}


$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "참기름으로 지출한 금액이 얼마야?"}'

$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "접시는?"}'

$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "치킨은?"}'
  
  
$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "여대 합계금액은 얼마야?"}'
  
  
$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "여대 합계금액에서 참기름값을 뺀 금액은 얼마야?"}'
  

```



```sh

$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "김기옥님이 찬조한 찬조품은?"}'

$ curl -X POST http://localhost:8000/knowledgeops/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "유기란님이 찬조한 찬조품은?"}'


```







### (3) rebuild

```sh

$ curl -X POST http://localhost:8000/knowledgeops/api/index/rebuild \

```





# 3. Dockerizing



## 1) dockerfile

```dockerfile
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


```



## 2) dockerizing

```sh

$ docker build -t knowledgeops-api /Users/song/Documents/GitRepo/GithubRepo/cloud-ai-lab/5_rag/labs/lab04_faiss_vector_rag/ 2>&1


```



## 3) docker

```sh
$ docker run -d \
  --name knowledgeops \
  -p 8000:8000 \
  --env-file /Users/song/Documents/GitRepo/GithubRepo/cloud-ai-lab/5_rag/labs/lab04_faiss_vector_rag/.env \
  -v /Users/song/Documents/GitRepo/GithubRepo/cloud-ai-lab/5_rag/labs/lab04_faiss_vector_rag/faiss_index:/app/faiss_index \
  knowledgeops-api && echo "컨테이너 시작됨"



```

