from pydantic import BaseModel

class SearchResults(BaseModel):
    """
    Represents the response from a search query.
    """
    title: str
    url: str
    content: str

class SearchResponse(BaseModel):
    """
    Represents the response from a search query.
    """
    results: list[SearchResults]
    """
    A list of search results.
    """
    costs: float