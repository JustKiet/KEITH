from app.core.interfaces import BaseVectorRepository
from app.core.models.milvus_entity import MilvusEntity
from app.core.models.milvus_add import MilvusAdd
from app.core.models.milvus_query import MilvusQueryOutput
from pymilvus import MilvusClient, CollectionSchema
from typing import overload, Optional

class MilvusRepository(BaseVectorRepository):
    def __init__(self, 
                 client: MilvusClient,
                 collection_name: str,
                 schema: CollectionSchema,
                 metric_type: str = "COSINE",
                 ):
        self.client = client

        self.collection_name = collection_name

        if not self.client.has_collection(collection_name):
            index_params = self.client.prepare_index_params()

            index_params.add_index(
                field_name="vector",
                index_name="vector_index",
                index_type="AUTOINDEX",
                metric_type=metric_type,
            )
            
            self.client.create_collection(
                collection_name=collection_name,
                schema=schema,
                index_params=index_params,
            )

    def add_vectors(
        self,
        vectors: list[list[float]],
        texts: list[str],
        metadatas: Optional[list[dict]] = None
    ) -> MilvusAdd:
        if not (len(vectors) == len(texts)):
            raise ValueError("vectors and texts must have the same length")

        # Find expected vector length from the first valid vector
        expected_len = None
        for vec in vectors:
            if isinstance(vec, list) and len(vec) > 0:
                expected_len = len(vec)
                break

        if expected_len is None:
            raise ValueError("No valid vectors found to determine expected dimension")

        for idx, vec in enumerate(vectors):
            if not isinstance(vec, list):
                raise TypeError(f"Vector at index {idx} is not a list")
            if len(vec) != expected_len:
                raise ValueError(f"Vector at index {idx} has length {len(vec)} but expected {expected_len}")

        if metadatas is None:
            entities = [
                MilvusEntity(
                    vector=vec,
                    text=txt,
                )
                for vec, txt in zip(vectors, texts)
            ]
        else:
            # Build vector entities with metadata unpacked to top-level fields
            entities = [
                MilvusEntity(
                    vector=vec,
                    text=txt,
                    **meta
                )
                for vec, txt, meta in zip(vectors, texts, metadatas)
            ]

        res = self.client.insert(
            collection_name=self.collection_name,
            data=[entity.model_dump() for entity in entities]
        )

        return MilvusAdd(
            insert_count=res["insert_count"],
            ids=res["ids"],
            cost=res["cost"]
        )
    
    def query_vectors(
        self,
        query_vector: list[float],
        top_k: int = 10,
        output_fields: Optional[list[str]] = ["text"]
    ) -> list[MilvusQueryOutput]:
        
        self.client.load_collection(
            collection_name=self.collection_name
        )
        
        res = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            anns_field="vector",
            limit=top_k,
            output_fields=output_fields
        )

        # Flatten the list of lists of dicts into a list of dicts
        res = [item for sublist in res for item in sublist]

        return [MilvusQueryOutput(**item) for item in res]
    
    @overload
    def delete_vectors(
        self,
        ids: list[int]
    ) -> dict:
        ...

    @overload
    def delete_vectors(
        self,
        filter: str
    ) -> dict:
        ...

    def delete_vectors(
        self,
        ids: Optional[list[int]] = None,
        filter: Optional[str] = None,
    ):
        if ids is None and filter is None:
            raise ValueError("Either ids or filter must be provided")
        
        if ids is not None and filter is not None:
            raise ValueError("Either ids or filter must be provided, but not both.")

        if ids is not None:
            res = self.client.delete(
                collection_name=self.collection_name, 
                ids=ids
            )
            return res
        
        elif filter is not None:
            res = self.client.delete(
                collection_name=self.collection_name, 
                filter=filter
            )
            return res
        
    def describe_collection(self) -> dict:
        return self.client.describe_collection(
            collection_name=self.collection_name
        )

    def drop_collection(self) -> dict:
        self.client.drop_collection(
            collection_name=self.collection_name
        )

        return {"message": f"Collection {self.collection_name} dropped successfully"}