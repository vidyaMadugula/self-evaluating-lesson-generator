import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

generator_llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60,
    max_retries=1
)

evaluator_llm = ChatGroq(
    model=os.getenv("GROQ_EVALUATOR_MODEL"),
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY"),
    timeout=60,
    max_retries=1
)