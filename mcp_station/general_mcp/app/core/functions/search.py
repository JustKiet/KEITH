import os
import requests
import asyncio
from typing import List
from typing import Literal

from app.schemas.search_response import SearchResponse, SearchResults 
from app.clients.openai_clients import ASYNC_OPENAI_CLIENT
from app.core.config import settings

async def summarize_content(content: str) -> tuple[str, float]:
    response = await ASYNC_OPENAI_CLIENT.chat.completions.create(
        model=settings.SEARCH_SUMMARIZATION_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an extraordinary assistant that summarizes content perfectly."
            },
            {
                "role": "user",
                "content": f"Summarize the following content, keep all core details: {content}"
            }
        ],
        temperature=0.0,
    )

    cost = ((response.usage.prompt_tokens - response.usage.prompt_tokens_details.cached_tokens) * (0.1 / 1_000_000))
    + (response.usage.completion_tokens * (0.4 / 1_000_000))
    + (response.usage.prompt_tokens_details.cached_tokens * ((0.1 / 1_000_000) / 2))

    return response.choices[0].message.content, cost

async def tavily_search(query: str, topic: Literal["general", "news"]) -> List[SearchResponse]:
    """
    Search using Tavily API and summarize content using OpenAI asynchronously.

    Args:p
        query (str): The search query. Try to search accordingly to the user's intent and region for the best results. Avoid acronyms, always write the full name.
        topic (Literal["general", "news"]): The topic of the search. Use "news" for news-related searches and "general" for any other topic.
    Returns:
        List[SearchResponse]: A list of search results with summarized content.
    """
    url = "https://api.tavily.com/search"
    payload = {
        "query": query,
        "topic": topic,
        "search_depth": "basic",
        "chunks_per_source": 3,
        "max_results": 2,
        "time_range": None,
        "days": 7,
        "include_answer": False,
        "include_raw_content": True,
        "include_images": False,
        "include_image_descriptions": False,
        "include_domains": [],
        "exclude_domains": []
    }
    headers = {
        "Authorization": f"Bearer {os.getenv('TAVILY_API_KEY')}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    outputs = response.json()["results"]

    # Summarize content and gather both summaries and costs
    tasks = [summarize_content(output["raw_content"]) for output in outputs]
    summaries_with_costs = await asyncio.gather(*tasks)
    summaries, costs = zip(*summaries_with_costs)  # unzip the list of tuples

    # Replace raw content with summaries
    for output, summary in zip(outputs, summaries):
        output["raw_content"] = summary

    return SearchResponse(
        results=[
            SearchResults(
                title=output.get("title"),
                url=output.get("url"),
                content=output.get("raw_content")
            )
            for output in outputs
        ],
        costs=sum(costs)
    )