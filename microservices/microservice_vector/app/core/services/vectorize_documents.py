from app.infrastructure.openagentkit.core.interfaces import BaseEmbeddingModel
from app.infrastructure.openagentkit.core.models.responses.embedding_response import EmbeddingUnit
from app.core.models.pdf_documents import PDFChunkVectorized, PDFDocumentWithChunks, PDFDocumentWithVectorizedChunks

def vectorize_documents(
    chunked_documents: list[PDFDocumentWithChunks],
    embedding_model: BaseEmbeddingModel,
) -> list[PDFDocumentWithVectorizedChunks]:
    vectorized_docs: list[PDFDocumentWithVectorizedChunks] = []

    for document in chunked_documents:
        vectorized_chunks: list[PDFChunkVectorized] = []
        embeddings: list[EmbeddingUnit] = embedding_model.encode_texts([chunk.content for chunk in document.chunks])

        for chunk, embedding in zip(document.chunks, embeddings):
            vectorized_chunks.append(
                PDFChunkVectorized(
                    content=chunk.content,
                    chunk_number=chunk.chunk_number,
                    page_from=chunk.page_from,
                    page_to=chunk.page_to,
                    embedded_vector=embedding.embedding,
                    embedding_type=embedding.type,
                    embedding_model=embedding_model.embedding_model,
                )
            )

        vectorized_docs.append(
            PDFDocumentWithVectorizedChunks(
                file_name=document.file_name,
                chunks=vectorized_chunks,
                embedding_type=embedding_model.encoding_format,
            )
        )

    return vectorized_docs