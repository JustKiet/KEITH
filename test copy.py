from mcp import ClientSession
from openagentkit.modules.openai import AsyncOpenAIExecutor
from openagentkit.core.utils.tool_wrapper import tool
from typing import Annotated
from mcp.client.sse import sse_client
import openai
import json
import os

async def run():
    async with sse_client("http://localhost:8088/sse") as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            
            await session.initialize()

            executor = AsyncOpenAIExecutor(
                client=openai.AsyncOpenAI(
                    api_key=os.environ.get("OPENAI_API_KEY"),
                ),
                model="gpt-4o-mini",
                system_message="You are a helpful assistant.",
            )

            await executor.connect_to_mcp(mcp_session=session)

            generator = executor.stream_execute(
                messages=[
                    {
                        "role": "user",
                        "content": "Whats 3+3? Also tell me the weather in Hanoi today."
                    }
                ]
            )

            async for response in generator:
                if response.content:
                    print(response.content, end="", flush=True)

            history = executor.get_history()
            with open("history.json", "w") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
