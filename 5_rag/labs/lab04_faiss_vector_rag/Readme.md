

# 1. 개요

## 1) 개요

문자열 검색 ❌ → 임베딩 + 벡터 검색(FAISS) ⭕

즉,  👉 *“의미로 문서를 찾는다”* 를 직접 체감



```
문서들
 ↓ (임베딩)
벡터
 ↓ (FAISS)
유사도 검색
 ↓
관련 문서
 ↓
LLM
 ↓
답변
```





## 2) 왜 FAISS + 임베딩이 필요한가?



이전 단계에서 했던 검색은:

```
if word in doc["content"]:
```

❌ 문제:

- 단어가 다르면 못 찾음
- 표현이 달라지면 실패



### 예시

```
질문: "cloud-ai-lab의 목적은?"
문서: "cloud-ai-lab은 팀장 스터디 저장소이다"
```

👉 **단어는 다르지만 의미는 같음**

→ 문자열 검색 ❌

→ **임베딩 검색 ⭕**







# 2. Python venv



## 1) 가상환경 생성

macOS/Linux:

```bash
python3 -m venv venv
```



## 2) 가상환경 활성화

**macOS/Linux:**

```bash
source venv/bin/activate
```

활성화되면 터미널 프롬프트 앞에 `(venv)`가 표시됩니다.



## 3) 필요한 패키지 설치

```
pip install langchain langchain-openai faiss-cpu
```

> GPU ❌

> CPU FAISS로 충분



## 4) 가상환경 비활성화

작업이 끝나면:

```bash
deactivate
```





# 3. 문서 준비



```
documents = [
    "cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다.",
    "LangChain은 LLM 기반 애플리케이션을 구성하기 위한 프레임워크이다.",
    "MCP는 LLM이 외부 시스템을 안전하게 호출하도록 돕는 프로토콜이다."
]
```





# 4. 임베딩 생성 (핵심)



```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
```

이 한 줄이 의미하는 것:

> 문장을 **숫자 벡터(의미 좌표)** 로 바꾼다





# 5. FAISS 벡터 스토어 생성



```
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_texts(
    texts=documents,
    embedding=embeddings
)
```

📌 이 순간:



- 문서 → 벡터
- FAISS 인덱스 생성 완료





------





# 6. 🔍 벡터 검색 (Retrieval)



```
query = "cloud-ai-lab의 목적은 뭐야?"

retrieved_docs = vectorstore.similarity_search(query, k=1)

context = "\n".join([doc.page_content for doc in retrieved_docs])

print("🔍 검색된 문서:")
print(context)
```

* k는 유사도 검색에서 반환할 문서 갯수이다.
  * documentes 에는 3개의 문서(3개의 문장 배열)가 있는 셈이다.

### 핵심 포인트

질문에:

- cloud-ai-lab
- 목적

이 정확히 없어도

👉 **의미상 가장 가까운 문서가 선택됨**





# 7. 이제 RAG로 연결



```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = \
ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    아래 문서를 참고해서 질문에 답해라.
    문서에 없는 내용은 모른다고 말해라.

    문서:
    {context}

    질문:
    {question}
    """
)

rag_chain = prompt | llm | StrOutputParser()
```





# 8. 전체 실행 코드



```
question = "cloud-ai-lab의 목적은 뭐야?"

retrieved_docs = vectorstore.similarity_search(question, k=1)
context = "\n".join([doc.page_content for doc in retrieved_docs])

result = rag_chain.invoke({
    "context": context,
    "question": question
})

print("🤖 답변:")
print(result)
```



```python
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.callbacks import get_openai_callback

load_dotenv()

FAISS_INDEX_PATH = "faiss_index"

embeddings = OpenAIEmbeddings()

if os.path.exists(FAISS_INDEX_PATH):
    print("📂 저장된 벡터 인덱스를 로드합니다.")
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    print("🔄 벡터 인덱스를 새로 생성합니다.")
    documents = [
        "1.cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다.",
        "2.LangChain은 LLM 기반 애플리케이션을 구성하기 위한 프레임워크이다.",
        "3.MCP는 LLM이 외부 시스템을 안전하게 호출하도록 돕는 프로토콜이다."
    ]
    import openai
    client = openai.OpenAI()
    response = client.embeddings.create(input=documents, model="text-embedding-ada-002")
    print(f"📊 [인덱스 생성] 토큰: {response.usage.total_tokens}")
    vectorstore = FAISS.from_texts(texts=documents, embedding=embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("💾 벡터 인덱스를 저장했습니다.")

question = "cloud-ai-lab의 목적은 뭐야?"
#question = "AI 스터디를 위해 만든 저장소는?"
#question = "MCP는 무엇인가?"

import openai
client = openai.OpenAI()
response = client.embeddings.create(input=[question], model="text-embedding-ada-002")
print(f"📊 [질문 임베딩] 토큰: {response.usage.total_tokens}")
retrieved_docs = vectorstore.similarity_search(question, k=1)

context = "\n".join([doc.page_content for doc in retrieved_docs])

print("🔍 검색된 문서:")
print(context)


from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = \
ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    아래 문서를 참고해서 질문에 답해라.
    문서에 없는 내용은 모른다고 말해라.

    문서:
    {context}

    질문:
    {question}
    """
)

rag_chain = prompt | llm | StrOutputParser()

with get_openai_callback() as cb:
    result = rag_chain.invoke({
        "context": context,
        "question": question
    })
    print(f"📊 [LLM] 토큰: {cb.total_tokens} (입력: {cb.prompt_tokens}, 출력: {cb.completion_tokens}), 비용: ${cb.total_cost:.6f}")

print("🤖 답변:")
print(result)




```







# 9. 우회 질문

일부로 이렇게 조회해도 해당 문서가 잘 선택된다.



```
question = "AI 스터디를 위해 만든 저장소는?"
```

👉 **단어 하나도 안 겹치는데**

👉 cloud-ai-lab 문서가 선택됨



이게 바로:

> **임베딩 기반 Retrieval**





# 10. 핵심 3가지



### ① 임베딩 = 의미 좌표

- 단어 ❌
- 의미 ⭕️



### ② FAISS = 빠른 벡터 검색 엔진

- In-memory
- 로컬 실습 최적



### ③ RAG 책임 분리

```
검색 정확도 = 임베딩 + 벡터DB
답변 품질   = 프롬프트 + LLM
```



# 11. cloud-ai-lab 추천 정리 구조



```
cloud-ai-lab/
└─ 4_rag/
   └─ lab03_faiss_vector_rag/
      ├─ main.py
      └─ README.md
```



### **README.md 핵심 문장**

```
이 실습은 문자열 검색이 아닌
의미 기반 벡터 검색으로 Retrieval을 수행한다.
```







# **🔑 한 줄 요약 (스터디용)**





> **RAG의 성능은 LLM이 아니라**

> **“임베딩 + 벡터 검색”이 70%를 결정한다.**



------



