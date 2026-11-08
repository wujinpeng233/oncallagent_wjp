import os

from dotenv import load_dotenv
from langchain_community.embeddings import DashScopeEmbeddings

load_dotenv()

def create_embedding_service()-> DashScopeEmbeddings:
    api_key = os.getenv("DASHSCOPE_API_KEY")

    if not api_key:
        raise RuntimeError("DASHSCOPE_API_KEY is not configured")


    return DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=api_key,
)