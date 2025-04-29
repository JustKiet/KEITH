import json
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich import box 
from rich.live import Live
from rich.spinner import Spinner
from rich.console import Group

from KEITH.core.agent import KEITH
from KEITH.services.auth import authenticate
from KEITH.exceptions import AuthenticationError

from mcp import ClientSession
from mcp.client.sse import sse_client
import traceback

import asyncio

import datetime

console = Console()

def display_welcome(username: str) -> None:
    """Display a welcome message."""
    # Create styled Text objects for title, subtitle, and welcome message
    title = Text("🤖 K.E.I.T.H", style="bold #59A5D8")
    subtitle = Text("Knowledge-Enhanced Intelligent Task Helper", style="#9BE7F7")
    
    # Create the welcome message using Text, and apply styles to parts of the text
    welcome_text = Text(f"""
    Welcome Mr. {username}!
    
    - Today's date: {datetime.datetime.now().strftime('%Y-%m-%d')}
    - Current time: {datetime.datetime.now().strftime('%H:%M:%S')}
    - Current weather: Sunny, 25°C (example)
    """, style="default")

    # Combine them all into one Text object, each part styled correctly
    panel_content = Text()
    panel_content.append(title)
    panel_content.append("\n")
    panel_content.append(subtitle)
    panel_content.append("\n\n")
    panel_content.append(welcome_text)
    
    # Print everything inside a panel
    console.print(Panel(
        panel_content,
        box=box.ROUNDED,
        style="#E6FAFF",
        border_style="#84D2F6",
        padding=(1, 2),
        title="Welcome"
    ))

async def chatloop():
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold #386FA4]You[/bold #386FA4]")
            
            # Check for exit commands
            if user_input.lower() in ('exit', 'quit', 'bye'):
                # Save conversation before exiting
                history = KEITH.get_history()
                filename = "conversation_history.json"
                
                with open(filename, "w") as f:
                    json.dump(history, f, ensure_ascii=False, indent=4)
                console.print(f"\n[green]Conversation saved to:[/green] {filename}")
                console.print("[bold cyan]Thank you for chatting! Goodbye![/bold cyan]")
                break
            
            # Get and display response
            response = KEITH.stream_execute(
                messages=[
                    {"role": "user", "content": user_input}
                ],
            )
            streamed_content = ""
            tool_results_content = ""
            tool_results_rendered = False

            with Live(console=console, refresh_per_second=60) as live:
                async for event in response:
                    renderables = []
                    # Handle tool_results once, shown at the top
                    if not tool_results_rendered and event.tool_results:
                        tool_results_content = str(event.tool_results)  # format as needed
                        tool_results_rendered = True
                    if tool_results_content:
                        tool_panel = Panel(
                            Markdown(tool_results_content[:150] + "..."),
                            box=box.ROUNDED,
                            style="#E6FAFF",
                            border_style="#133C55",
                            title="🔧 Tool Result",
                            padding=(1, 2),
                        )
                        renderables.append(tool_panel)
                    # Handle streamed delta content below
                    if event.delta_content:
                        streamed_content += event.delta_content
                    response_panel = Panel(
                        Markdown(streamed_content),
                        box=box.ROUNDED,
                        style="#E6FAFF",
                        border_style="#84D2F6",
                        title="🤖 K.E.I.T.H",
                        padding=(1, 2),
                    )
                    renderables.append(response_panel)
                    # Update both panels together, stacked
                    live.update(Group(*renderables))
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Chat terminated by user.[/bold red]")
            # Save conversation before exiting
            history = KEITH.get_history()
            filename = "conversation_history.json"
            
            with open(filename, "w") as f:
                json.dump(history, f, ensure_ascii=False, indent=4)
            
            console.print(f"[green]Conversation saved to:[/green] {filename}")
            break
        
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            traceback.print_exc()
                    
async def main():
    username = Prompt.ask("Enter your username")
    password = Prompt.ask("Enter your password", password=True)

    if not authenticate(username=username, password=password):
        raise AuthenticationError("Invalid username or password. Please try again.")

    console.clear()

    display_welcome(username)

    async with sse_client("http://127.0.0.1:8088/sse") as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            
            await session.initialize()

            await KEITH.connect_to_mcp(mcp_session=session)

            await chatloop()

if __name__ == "__main__":
    asyncio.run(main())