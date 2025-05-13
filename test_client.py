from mcp import ClientSession
from mcp.client.sse import sse_client
import json

class AsyncMultiContextWrapper:
    def __init__(self, **named_ctx_managers):
        self._ctx_managers = named_ctx_managers
        self.resources = {}

    async def open(self):
        self.resources = {}
        for name, ctx in self._ctx_managers.items():
            self.resources[name] = await ctx.__aenter__()
        return self.resources

    async def close(self, exc_type=None, exc_val=None, exc_tb=None):
        for name, ctx in reversed(self._ctx_managers.items()):
            await ctx.__aexit__(exc_type, exc_val, exc_tb)

async def run():
    wrapper = AsyncMultiContextWrapper(
        sse=sse_client("http://localhost:8088/sse")
    )

    resources = await wrapper.open()
    read, write = resources["sse"]

    session = ClientSession(read, write)
    await session.__aenter__()  # manually enter it

    try:
        initialize_result = await session.initialize()
        tools = await session.list_tools()
        print("Initialize Result:", json.dumps(initialize_result.model_dump(), ensure_ascii=False, indent=4))
        print("Tools:", json.dumps(tools.model_dump(), ensure_ascii=False, indent=4))
    finally:
        await session.__aexit__(None, None, None)
        await wrapper.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())

