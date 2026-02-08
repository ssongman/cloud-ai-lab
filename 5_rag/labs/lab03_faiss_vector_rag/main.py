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


