from pydantic import BaseModel
from typing import Union, Literal

class PDFChunk(BaseModel):
    """
    Model representing a chunk of a PDF document.

    Attributes:
        content: The content of the PDF chunk.
        chunk_number: The chunk number of the PDF document.
        page_from: The starting page number of the chunk. (1-indexed)
        page_to: The ending page number of the chunk. (1-indexed)
    """
    content: str
    """
    The content of the PDF chunk.
    """
    chunk_number: int
    """
    The chunk number of the PDF document.
    """
    page_from: int
    """
    The starting page number of the chunk. (1-indexed)
    """
    page_to: int
    """
    The ending page number of the chunk. (1-indexed)
    """

class PDFChunkVectorized(PDFChunk):
    """
    A class representing a chunk of a PDF document with an embedded vector.
    
    Attributes:
        content: The content of the PDF chunk.
        chunk_number: The chunk number of the PDF document.
        page_from: The starting page number of the chunk. (1-indexed)
        page_to: The ending page number of the chunk. (1-indexed)
        embedded_vector: The embedded vector representation of the PDF document.
        embedding_model: The name of the embedding model used for generating the embedded vector.
    """
    embedded_vector: Union[list[float], str]
    """
    The embedded vector representation of the PDF document.
    """
    embedding_type: Literal["base64", "float"]
    """
    The type of the embedded vector representation. Is either "base64" or "float".
    """
    embedding_model: str
    """
    The name of the embedding model used for generating the embedded vector.
    """

class PDFDocumentWithChunks(BaseModel):
    """
    A class representing a PDF document with its chunks.
    
    Attributes:
        file_name: The filename of the PDF document.
        chunks: The list of chunks for the PDF document.
    """
    file_name: str
    """
    The filename of the PDF document.
    """
    chunks: list[PDFChunk]
    """
    The list of chunks for the PDF document.
    """

class PDFDocumentWithVectorizedChunks(BaseModel):
    """
    A class representing a PDF document with its vectorized chunks.
    
    Attributes:
        file_name: The filename of the PDF document.
        chunks: The list of vectorized chunks for the PDF document.
        embedding_type: The type of the embedded vector representation. Is either "base64" or "float".
    """
    file_name: str
    """
    The filename of the PDF document.
    """
    chunks: list[PDFChunkVectorized]
    """
    The list of vectorized chunks for the PDF document.
    """
    embedding_type: Literal["base64", "float"]
    """
    The type of the embedded vector representation. Is either "base64" or "float".
    """