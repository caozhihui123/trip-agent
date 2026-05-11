"""LLM 工厂 — LangChain ChatOpenAI"""
from langchain_openai import ChatOpenAI
from app.config import LLM_API_KEY, LLM_MODEL, LLM_BASE_URL


def create_chat_model(temperature: float = 0.7) -> ChatOpenAI:
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        temperature=temperature,
        timeout=120,
        max_retries=2,
    )
