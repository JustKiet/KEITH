from typing import Annotated
from openagentkit.core.utils.tool_wrapper import tool

@tool(
    description="Use this tool to retrieve documents from the knowledge base.",
)
def retrieve_knowledge_base(
    query: Annotated[str, "The query to search for."],
) -> dict:
    """
    Retrieve the top K documents from Milvus based on the query.
    
    Args:
        query (str): The query to search for.
        top_k (int): The number of top documents to retrieve.
        collection_name (str): The name of the collection in Milvus.
        embedding_model (str): The embedding model to use.
    
    Returns:
        dict: A dictionary containing the retrieved documents.
    """
    from KEITH.shared.clients import MILVUS_CLIENT, EMBEDDING_MODEL
    query_embedding = EMBEDDING_MODEL.encode_query(query)
    # Implement the retrieval logic here
    res = MILVUS_CLIENT.search(
        collection_name="demo_collection",
        data=[query_embedding.embedding],
        limit=2,
        output_fields=["content", "page", "file_name"],
    )
    return res