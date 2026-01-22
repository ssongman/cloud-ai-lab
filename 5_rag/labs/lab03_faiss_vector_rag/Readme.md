좋아요 👍

이제 **“진짜 RAG”의 핵심 단계**로 들어갑니다.



> 🎯 목표

> **문자열 검색 ❌ → 임베딩 + 벡터 검색(FAISS) ⭕**

> 즉,

> 👉 *“의미로 문서를 찾는다”* 를 직접 체감



아래 가이드는 **30분 이내**, **최소 코드**, **개념이 눈에 보이게** 구성했습니다.



------





# **0️⃣ 오늘 완성할 구조**



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



------





# **1️⃣ 왜 FAISS + 임베딩이 필요한가?**



이전 단계에서 했던 검색은:

```
if word in doc["content"]:
```

❌ 문제:

- 단어가 다르면 못 찾음
- 표현이 달라지면 실패



### **예시**

```
질문: "cloud-ai-lab의 목적은?"
문서: "cloud-ai-lab은 팀장 스터디 저장소이다"
```

👉 **단어는 다르지만 의미는 같음**

→ 문자열 검색 ❌

→ **임베딩 검색 ⭕**







# **2️⃣ 준비물 설치**



```
pip install langchain langchain-openai faiss-cpu
```

> GPU ❌

> CPU FAISS로 충분





# **3️⃣ 문서 준비 (여러 개)**



```
documents = [
    "cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다.",
    "LangChain은 LLM 기반 애플리케이션을 구성하기 위한 프레임워크이다.",
    "MCP는 LLM이 외부 시스템을 안전하게 호출하도록 돕는 프로토콜이다."
]
```



------





# **4️⃣ 임베딩 생성 (핵심)**



```
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
```

이 한 줄이 의미하는 것:



> 문장을 **숫자 벡터(의미 좌표)** 로 바꾼다



------





# **5️⃣ FAISS 벡터 스토어 생성**



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





# **6️⃣ 🔍 벡터 검색 (Retrieval)**



```
query = "cloud-ai-lab의 목적은 뭐야?"

retrieved_docs = vectorstore.similarity_search(query, k=1)

context = "\n".join([doc.page_content for doc in retrieved_docs])

print("🔍 검색된 문서:")
print(context)
```



### **여기서** 

### **체감 포인트**





질문에:



- cloud-ai-lab
- 목적





이 정확히 없어도

👉 **의미상 가장 가까운 문서가 선택됨**



------





# **7️⃣ 이제 RAG로 연결**



```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")

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



------





# **8️⃣ 전체 실행 코드 (🔥 완성)**



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



------





# **9️⃣ 일부러 이렇게 질문해 보세요 (체감용)**



```
question = "AI 스터디를 위해 만든 저장소는?"
```

👉 **단어 하나도 안 겹치는데**

👉 cloud-ai-lab 문서가 선택됨



이게 바로:



> **임베딩 기반 Retrieval**



------





# **10️⃣ 오늘 반드시 이해해야 할 핵심 3가지**







### **① 임베딩 = 의미 좌표**





- 단어 ❌
- 의미 ⭕️







### **② FAISS = 빠른 벡터 검색 엔진**





- In-memory
- 로컬 실습 최적







### **③ RAG 책임 분리**



```
검색 정확도 = 임베딩 + 벡터DB
답변 품질   = 프롬프트 + LLM
```



------





# **11️⃣ cloud-ai-lab 추천 정리 구조**



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



------





# **🔑 한 줄 요약 (스터디용)**





> **RAG의 성능은 LLM이 아니라**

> **“임베딩 + 벡터 검색”이 70%를 결정한다.**



------





## **다음 단계 (이제 진짜 재미있는 구간)**





이제 선택지는 딱 3개입니다 👇



1️⃣ **RAG 성능 튜닝 (k, chunk, overlap)**

2️⃣ **RAG + Agent (질문 유형 분기)**

3️⃣ **RAG + MCP (사내 데이터 연결)**



👉 다음으로 **몇 번** 갈까요?