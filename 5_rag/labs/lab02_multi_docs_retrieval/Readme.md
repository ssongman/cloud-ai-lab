좋아요 👍

그럼 **1번: “문서 여러 개 → 검색 단계 추가”** 를

**최소 코드 + 최대 체감**으로 바로 진행할게요.



> ❗ 목표는 **“아, Retrieval이 이거구나”** 를 느끼는 것

> 벡터DB ❌, 임베딩 ❌, FAISS ❌

> → **순수 Python 검색**



------





# **🎯 오늘 목표 (10분)**





> **여러 문서 중에서**

> **질문과 관련된 문서만 골라서 LLM에게 주기**



------





# **0️⃣ 구조 먼저 보기 (이게 RAG의 뼈대)**



```
질문
 ↓
문서 검색 (Retrieval)
 ↓
선택된 문서
 ↓
LLM
 ↓
답변
```



------





# **1️⃣ 문서 여러 개 준비**



```python
documents = [
    {
        "id": 1,
        "content": "cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다."
    },
    {
        "id": 2,
        "content": "LangChain은 LLM 기반 애플리케이션을 구성하기 위한 프레임워크이다."
    },
    {
        "id": 3,
        "content": "MCP는 LLM이 외부 시스템을 안전하게 호출하도록 돕는 프로토콜이다."
    }
]
```



------





# **2️⃣ 🔍 초간단 Retrieval 함수 만들기**





> 질문에 **키워드가 포함된 문서만 선택**

```python
def retrieve_docs(question, docs):
    results = []
    for doc in docs:
        if any(word in doc["content"] for word in question.split()):
            results.append(doc["content"])
    return "\n".join(results)
```

📌 **이게 바로 Retrieval**

(지금은 단순하지만, 나중에 벡터 검색으로 교체됨)



------





# **3️⃣ LLM + RAG 체인**



```python
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





# **4️⃣ 전체 실행 코드 (🔥 핵심)**



```python

question = "cloud-ai-lab은 뭐야?"

context = retrieve_docs(question, documents)

print("🔍 선택된 문서:")
print(context)
print("-" * 40)

result = rag_chain.invoke({
    "context": context,
    "question": question
})

print("🤖 답변:")
print(result)
```



------



## 전체 코드

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


def retrieve_docs(question, docs):
    results = []
    for doc in docs:
        if any(word in doc["content"] for word in question.split()):
            results.append(doc["content"])
    return "\n".join(results)
  
  
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



documents = [
    {
        "id": 1,
        "content": "cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다."
    },
    {
        "id": 2,
        "content": "LangChain은 LLM 기반 애플리케이션을 구성하기 위한 프레임워크이다."
    },
    {
        "id": 3,
        "content": "MCP는 LLM이 외부 시스템을 안전하게 호출하도록 돕는 프로토콜이다."
    }
]




question = "cloud-ai-lab은 뭐야?"

context = retrieve_docs(question, documents)

print("🔍 선택된 문서:")
print(context)
print("-" * 40)

result = rag_chain.invoke({
    "context": context,
    "question": question
})

print("🤖 답변:")
print(result)

    
    
```







# **5️⃣ 실행 결과**



### **출력 예시**

```

$ python main.py 
🔍 선택된 문서:
cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다.
----------------------------------------
🤖 답변:
cloud-ai-lab은 Cloud사업담당 팀장들이 AI 기술을 학습하기 위한 스터디 저장소이다.

```

👉 **다른 문서는 무시됨**

👉 질문에 필요한 문서만 선택됨





# **6️⃣ 일부러 질문 바꿔보기 (중요)**



```
question = "MCP는 뭐야?"
```

🔍 선택된 문서가 바뀌고

🤖 답변도 바뀜



```sh

$ python main.py
🔍 선택된 문서:

----------------------------------------
🤖 답변:
죄송하지만 제가 참고할 문서가 없기 때문에 MCP가 무엇인지 알 수 없습니다. 다른 질문이 있으시다면 도와드리겠습니다.


```





# **7️⃣ 오늘 이 단계에서 반드시 이해해야 할 것 3가지**



### **① Retrieval은** 검색 로직

- 지금은 문자열 포함
- 나중엔 임베딩/벡터



### **② LLM은** 선택된 문서만 본다

- 다른 문서 존재 ❌



### **③ RAG의 책임 분리**

```
검색 = 코드
추론 = LLM
```





# 8️⃣ cloud-ai-lab 정리 구조 (추천)



```
cloud-ai-lab/
└─ 4_rag/
   └─ lab02_multi_docs_retrieval/
      ├─ main.py
      └─ README.md
```



### README.md 핵심 문장

```
이 실습은 RAG에서 Retrieval 단계가
LLM과 독립적으로 동작함을 이해하기 위한 예제이다.
```





# **🔑 한 줄 요약 (스터디용)**



> **RAG의 핵심은 “LLM이 답을 잘하느냐”가 아니라**

> **“어떤 문서를 보여주느냐”다.**

