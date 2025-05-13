from openagentkit.modules.openai import AsyncOpenAIExecutor
from app.core.resources.alfred_prompt import ALFRED
from app.core.config import settings

def get_keith_agent():
    from app.clients.openai_clients import OPENAI_CLIENT
    return AsyncOpenAIExecutor(
        client=OPENAI_CLIENT,
        temperature=1.0,
        model=settings.OPENAI_MODEL,
        system_message=ALFRED,
    )

KEITH_AGENT = get_keith_agent()
