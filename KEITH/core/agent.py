from openagentkit.modules.openai import AsyncOpenAIExecutor
from KEITH.tools import retrieve_knowledge_base
from KEITH.shared.clients import OPENAI_CLIENT
from KEITH.core.prompt import ALFRED

KEITH = AsyncOpenAIExecutor(
    client=OPENAI_CLIENT,
    temperature=1.0,
    model="gpt-4o-mini",
    system_message=ALFRED,
)