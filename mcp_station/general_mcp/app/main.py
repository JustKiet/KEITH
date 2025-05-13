from mcp.server.fastmcp import FastMCP
import uvicorn
import os
import multiprocessing

from app.core.functions import (
    get_weather_tool,
    tavily_search,
)

mcp = FastMCP("GeneralMCP")

app =mcp.sse_app()

mcp.add_tool(
    fn=get_weather_tool,
)

mcp.add_tool(
    fn=tavily_search,
)

if __name__ == "__main__":
    if os.getenv("RUNNING_IN_PRODUCTION"):
        # Production mode with multiple workers for better performance
        uvicorn.run(
            "main:app",  # Pass as import string
            host="0.0.0.0",
            port=8088,
            workers=(multiprocessing.cpu_count() * 2) + 1,
            timeout_keep_alive=300  # Increased for SSE connections
        )
    else:
        # Development mode with a single worker for easier debugging
        uvicorn.run("main:app", host="0.0.0.0", port=8088, reload=True)
