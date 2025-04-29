from openagentkit.modules.openai import OpenAIEmbeddingModel
from pymilvus import MilvusClient
import openai
import os

MILVUS_CLIENT = MilvusClient("milvus_database.db")

OPENAI_CLIENT = openai.AsyncOpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

EMBEDDING_MODEL = OpenAIEmbeddingModel(
    client=OPENAI_CLIENT,
)

