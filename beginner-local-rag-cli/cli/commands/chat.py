import click
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.chat import generate_response_streaming, ensure_model_pulled
from src.embeddings import get_embedding_model
from src.opensearch import hybrid_search
from src.constants import OLLAMA_MODEL_NAME

console = Console()

@click.command()
@click.option('--rag/--no-rag', default=True, help='Enable/disable RAG mode')
@click.option('--top-k', default=5, help='Number of documents to retrieve')
@click.option('--temperature', default=0.7, help='LLM temperature')
@click.option('--index-name', default='rag_index', help='OpenSearch index name')
def chat(rag, top_k, temperature, index_name):
    """Start an interactive chat session."""
    
    console.print(Panel.fit(
        "[bold cyan]Local RAG Chat System[/bold cyan]\n\n"
        f"Mode: {'RAG Enabled' if rag else 'Direct LLM'}\n"
        f"Model: {OLLAMA_MODEL_NAME}\n"
        f"Temperature: {temperature}\n\n"
        "[dim]Commands:[/dim]\n"
        "  • Type 'exit' or 'quit' to end\n"
        "  • Type 'clear' to clear history\n"
        "  • Ctrl+C to interrupt",
        border_style="cyan"
    ))
    
    # Ensure model is available
    with console.status("[bold green]Checking model availability..."):
        if not ensure_model_pulled(OLLAMA_MODEL_NAME):
            console.print("[red]Failed to load model. Please check Ollama installation.[/red]")
            raise click.Abort()
    
    # Load embedding model if RAG is enabled
    embedding_model = None
    if rag:
        with console.status("[bold green]Loading embedding model..."):
            embedding_model = get_embedding_model()
        console.print("[green]✓ RAG system ready[/green]\n")
    else:
        console.print("[yellow]⚠ RAG disabled - using direct LLM only[/yellow]\n")
    
    session = PromptSession(history=FileHistory('.chat_history'))
    chat_history = []
    
    while True:
        try:
            # Get user input
            user_input = session.prompt('\n[bold green]You[/bold green] ❯ ')
            
            if not user_input.strip():
                continue
                
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]Goodbye! 👋[/yellow]")
                break
            
            if user_input.lower() == 'clear':
                chat_history = []
                console.clear()
                console.print("[green]✓ Chat history cleared[/green]")
                continue
            
            # Retrieve context if RAG is enabled
            context = ""
            if rag and embedding_model:
                with console.status("[dim]Retrieving relevant documents...[/dim]"):
                    search_results = hybrid_search(
                        user_input, 
                        embedding_model, 
                        top_k, 
                        index_name
                    )
                    
                    if search_results:
                        context = "\n\n".join([
                            result['_source']['text'] 
                            for result in search_results
                        ])
                        console.print(f"[dim]Retrieved {len(search_results)} relevant chunks[/dim]")
            
            # Generate response
            console.print("\n[bold blue]Assistant[/bold blue] ❯ ", end="")
            
            response_text = ""
            for chunk in generate_response_streaming(
                user_input, 
                context, 
                chat_history, 
                temperature
            ):
                console.print(chunk, end="")
                response_text += chunk
            
            console.print()  # New line after response
            
            # Update history
            chat_history.append({
                "role": "user",
                "content": user_input
            })
            chat_history.append({
                "role": "assistant", 
                "content": response_text
            })
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠ Interrupted[/yellow]")
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye! 👋[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
