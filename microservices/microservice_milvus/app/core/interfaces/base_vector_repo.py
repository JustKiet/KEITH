from abc import ABC, abstractmethod
from app.core.models.milvus_add import MilvusAdd

class BaseVectorRepository(ABC):
    """
    Abstract base class for vector repositories
    This class defines the interface for vector repositories
    that can add vectors to a vector database, query vectors, and delete vectors

    Args:
        None

    Methods:
        add_vectors: Add vectors to the vector database
        query_vectors: Query vectors from the vector database
        delete_vectors: Delete vectors from the vector database
    """
    @abstractmethod
    def add_vectors(self, vectors: list[list[float]], texts: list[str], metadata: list[dict]) -> MilvusAdd:
        raise NotImplementedError
    
    @abstractmethod
    def query_vectors(self, query_vector: list[float], top_k: int, output_fields: list[str]) -> list[dict]:
        raise NotImplementedError
    
    @abstractmethod
    def delete_vectors(self, ids: list[str], filter: str) -> None:
        raise NotImplementedError