



# 1. 개요

langchain hello world





# 2. Container 환경 구축



```sh

$ docker ps

$ docker run -d --name python python sleep 365d

$ docker exec -it python bash
```





# 3. Langchain 환경설정



### LangChain 설치

```sh

$ pip install -U langchain langchain-core langchain-openai

```



### api key 연결

```sh
export OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxx"

```



# 4. Python 수행

## Step1 - LLM 단독 호출



```sh

mkdir ~/song
cd ~/song

cat > main.py



```



```python

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

print(llm.invoke("LangChain이 뭐야?"))

```



결과

```sh

$ python main.py

content='LangChain은 언어 서비스 및 기술을 제공하는 기업이나 플랫폼을 의미할 수 있습니다.컴퓨터 언어 및 프로그래밍언어에 사용되기도 한다. 
따라서 LangChain이 무엇을 의미하는지는 그 문맥에 따라서 달라질 수 있습니다.' 
additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 105, 'prompt_tokens': 14, 'total_tokens': 119, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'id': 'chatcmpl-CzI6qa7fshZRUg3mJXSkkFMhpX0f0', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019bd025-2a49-7be1-826c-cc8a91f480ea-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 14, 'output_tokens': 105, 'total_tokens': 119, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}


```



## Step2 - PromptTemplate

```sh

$ pip install langchain_core

$ cat > main2.py
```



```python

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    input_variables=["topic"],
    template="아래 주제에 대해 한 문장으로 설명해줘.\n주제: {topic}"
)

print(llm.invoke(prompt.format(topic="LangChain")))

```



```sh

# 결과
$ python main2.py

content='LangChain은 언어 간 상호 운용성을 제공하는 블록체인 기술로, 다양한 언어를 사용하는 사용자들 간의 원활한 소통과 협력을 돕는다.' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 65, 'prompt_tokens': 29, 'total_tokens': 94, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'gpt-3.5-turbo-0125', 'system_fingerprint': None, 'id': 'chatcmpl-CzID4uUqCtb4ILK2uV52kqWKR0UpN', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None} id='lc_run--019bd02b-0d90-7132-9534-b0859cd51a58-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 29, 'output_tokens': 65, 'total_tokens': 94, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}}

```





## Step 3 - LLMChain (핵심)

**Prompt + LLM**

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

llm = ChatOpenAI(model="gpt-3.5-turbo")

prompt = PromptTemplate(
    input_variables=["topic"],
    template="아래 주제에 대해 한 문장으로 설명해줘.\n주제: {topic}"
)

chain = prompt | llm

result = chain.invoke({"topic": "LangChain"})
print(result.content)


```



```sh
# 결과

LangChain은 자연어 처리 기술과 블록체인 기술을 결합하여 언어 장벽을 극복하고 신뢰할 수 있는 언어 서비스를 제공하는 플랫폼이다.

```





## Step 4 - 체인을 “연결”해보기 (진짜 LangChain)



```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")

# 1단계: 설명
explain_prompt = PromptTemplate(
    input_variables=["topic"],
    template="{topic}에 대해 간단히 설명해줘."
)

# 2단계: 요약
summary_prompt = PromptTemplate(
    input_variables=["text"],
    template="다음 내용을 한 줄로 요약해줘:\n{text}"
)

chain = (
    explain_prompt
    | llm
    | StrOutputParser()   # AIMessage → 문자열
    | summary_prompt
    | llm
    | StrOutputParser()
)

result = chain.invoke({"topic": "LangChain"})
print(result)
```



```sh

# 결과

LangChain은 다양한 언어를 사용하는 사용자들 간의 커뮤니케이션을 원활하게 만들기 위해 개발된 블록체인 기술이며, 통신, 번역 및 인터페이스의 언어 장벽을 제거하여 소통을 용이하게 만들어줍니다.

```

\

# 5. OpenAI SDK Sample

OpenAI SDK 와 비교해보자.  

```sh

$ pip install openai


$ cat > main11.py

```



```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5-nano",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)

```



```sh

# 결과
Under the silver moon, a gentle unicorn whispered goodnight to the sleeping stars and drifted off into dreamland.


```



## 결론... 

현재까지의 소스 수준으로는 LangChain은 OpenAI SDK 와 비교해서 별로 다를것이 없다.





# 6. LangChain 비교 예제



> **LangChain의 가치는 ‘LLM 호출’이 아니라**

> **‘LLM 주변의 복잡한 흐름을 코드로 조립하는 능력’에 있다.**





## 1) OpenAI SDK 방식의 한계 (의도적으로 늘려봄)

아래는 **현실적인 요구사항**을 OpenAI SDK만으로 처리하는 코드입니다.



### **요구사항**

1. 사용자 입력을 설명
2. 설명 결과를 요약
3. JSON으로 구조화
4. 실패 시 재시도
5. 중간 결과 재사용



### **OpenAI SDK 방식 (가독성 나쁨)**



```sh

$ cat > main21.py

```



```python
from openai import OpenAI
import json

client = OpenAI()

def call_llm(prompt):
    return client.responses.create(
        model="gpt-5-nano",
        input=prompt
    ).output_text

text = call_llm("LangChain에 대해 설명해줘.")

summary = call_llm(f"다음 내용을 한 문장으로 요약해줘:\n{text}")

json_result = call_llm(
    f"""
    아래 내용을 JSON으로 만들어줘.
    형식: {{ "summary": string }}
    내용: {summary}
    """
)

try:
    data = json.loads(json_result)
except:
    raise RuntimeError("JSON 파싱 실패")

print(data)
```

```sh

# 결과
{'summary': 'LangChain은 LLM을 실제 애플리케이션에 쉽게 연결해 주는 게이트웨이 라이브러리로, 데이터 소스·도구·기억·프롬프트 등을 엮어 복잡한 워크플로를 구성하고 Chains/Agents/Tools/Memory/Vector Stores 등 다양한 구성 요소로 RAG 같은 활용을 가능하게 한다.'}

```



👉 **동작은 하지만**



- 흐름이 눈에 안 들어옴
- 중간 단계 재사용 어려움
- RAG / Agent로 확장 거의 불가능





# 2) LangChain으로 “같은 요구사항”을 만든 코드



이제 **같은 기능을 LangChain으로** 만들어 보자.

```sh

cat > main22.py

```



```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

llm = ChatOpenAI(model="gpt-3.5-turbo")

explain = PromptTemplate(
    input_variables=["topic"],
    template="{topic}에 대해 설명해줘."
)

summarize = PromptTemplate(
    input_variables=["text"],
    template="다음 내용을 한 문장으로 요약해줘:\n{text}"
)

to_json = PromptTemplate(
    input_variables=["summary"],
    template='{{ "summary": "{summary}" }}'
)

chain = (
    explain
    | llm
    | summarize
    | llm
    | to_json
    | llm
    | JsonOutputParser()
)

print(chain.invoke({"topic": "LangChain"}))
```



# **3️⃣ “아!” 포인트 — LangChain의 진짜 장점**



## **🔥 장점 1.** 흐름이 눈에 보인다



```
설명 → 요약 → JSON 변환
```

이 흐름이 **코드 구조 그대로 드러남**



## **🔥 장점 2.** 중간 단계가 재사용 가능

```
explain_chain = explain | llm
```

이걸:

- RAG
- Agent
- LangGraph 노드

로 **그대로 재사용**



## **🔥 장점 3.** Output Parser = 안정성

```
JsonOutputParser()
```

- 문자열 파싱 ❌
- 구조 보장 ⭕
- Agent에서 필수





## **🔥 장점 4.** 확장 방향이 명확

지금 코드에서:

- LLM → 다른 모델로 교체
- Prompt → RAG Prompt로 교체
- llm → Tool Calling으로 교체





# **4️⃣ LangChain을 써야 “값어치”가 나는 대표 예제**



아래 중 **하나라도 필요하면 LangChain이 맞습니다.**

| **필요 기능** | **OpenAI SDK** | **LangChain** |
| ------------- | -------------- | ------------- |
| RAG           | ❌ 수작업       | ⭕ 기본 패턴   |
| Agent Loop    | ❌ 직접 구현    | ⭕ 자연스러움  |
| Tool 선택     | ❌ if/else      | ⭕ 구조적      |
| 상태 관리     | ❌ 직접         | ⭕ 연결        |
| 멀티 스텝     | ❌ 복잡         | ⭕ 직관적      |





# **5️⃣ 진짜 “체감 100%” 예제 (추천)**



### **RAG + Runnable 최소 예제**

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

docs = """
LangChain은 LLM 기반 애플리케이션을
구성하기 위한 프레임워크이다.
"""

prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""
    문서를 참고해서 질문에 답해라.

    문서:
    {context}

    질문:
    {question}
    """
)

chain = (
    prompt
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()
)

print(chain.invoke({
    "question": "LangChain은 무엇을 하는 도구야?",
    "context": docs
}))
```

👉 이 순간부터 **“SDK vs LangChain 차이”가 명확해짐**



------





# **6️⃣ 언제 LangChain을 쓰고, 언제 안 쓰나**



### **❌ LangChain 안 써도 되는 경우**

- 단발성 질문
- 1-step 응답
- PoC용 스크립트



### **⭕ LangChain 써야 하는 경우**

- RAG
- Agent
- MCP 연계
- 운영 자동화
- 멀티스텝 처리





# **7️⃣ 지금 당신의 상황에서의 정확한 결론**

> ✔ “지금까지의 예제는 일부러 단순했다”

> ✔ LangChain은 **단순할수록 가치가 안 보인다**

> ✔ 복잡해질수록 **차이가 폭발적으로 커진다**



------

