from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.config import OPENAI_MODEL

llm = ChatOpenAI(model=OPENAI_MODEL)

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""아래 문서를 참고해서 질문에 답해라.
문서에 없는 내용은 모른다고 말해라.
답변은 반드시 높임말로 해라.

문서:
{context}

질문:
{question}""",
)

rag_chain = prompt | llm | StrOutputParser()
