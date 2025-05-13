from app.core.models.milvus_query import MilvusQueryOutput, MilvusRerankOutput
from app.deps import RERANKER_MODEL
    
def rerank_responses(
    query: str,
    responses: list[MilvusQueryOutput],
    rerank_top_k: int = 5,
) -> list[MilvusRerankOutput]:
    if rerank_top_k > len(responses):
        raise ValueError(f"rerank_top_k ({rerank_top_k}) must be less than or equal to the number of responses ({len(responses)})")

    texts = [response.entity.text for response in responses]

    reranked_responses = RERANKER_MODEL(
        query=query,
        documents=texts,
        top_k=rerank_top_k,
    )

    reranked_responses = [
        MilvusRerankOutput(
            score=reranked.score,
            text=texts[reranked.index],
        )
        for reranked in reranked_responses
    ]

    return reranked_responses