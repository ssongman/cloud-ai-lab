

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
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000

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

