import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.callbacks import get_openai_callback
from langchain_community.document_loaders import PyPDFLoader

load_dotenv()

PDF_PATH = "25년의용소방대결산.pdf"
FAISS_INDEX_PATH = "faiss_index_fire"

embeddings = OpenAIEmbeddings()

if os.path.exists(FAISS_INDEX_PATH):
    print("📂 저장된 벡터 인덱스를 로드합니다.")
    vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
else:
    print("🔄 PDF를 로드하고 벡터 인덱스를 새로 생성합니다.")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load_and_split()
    print(f"📄 PDF 페이지 수: {len(documents)}")
    vectorstore = FAISS.from_documents(documents=documents, embedding=embeddings)
    vectorstore.save_local(FAISS_INDEX_PATH)
    print("💾 벡터 인덱스를 저장했습니다.")

question = "고체연료로 지출한 금액이 얼마야?"

retrieved_docs = vectorstore.similarity_search(question, k=3)

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


