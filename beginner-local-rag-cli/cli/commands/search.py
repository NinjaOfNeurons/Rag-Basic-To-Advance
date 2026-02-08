import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.opensearch import hybrid_search
from src.embeddings import get_embedding_model

console = Console()

@click.command()
@click.argument('query')
@click.option('--top-k', default=5, help='Number of results')
@click.option('--index-name', default='rag_index', help='OpenSearch index name')
def search(query, top_k, index_name):
    """Search for documents using hybrid search."""
    
    console.print(Panel.fit(
        f"[bold]Query:[/bold] {query}\n"
        f"[dim]Index: {index_name} | Top-K: {top_k}[/dim]",
        border_style="blue"
    ))
    
    try:
        # Get embedding model
        with console.status("[bold green]Loading embedding model..."):
            model = get_embedding_model()
        
        # Perform hybrid search
        with console.status("[bold green]Searching..."):
            results = hybrid_search(query, model, top_k, index_name)
        
        if not results:
            console.print("[yellow]No results found[/yellow]")
            return
        
        # Create results table
        table = Table(
            title=f"Search Results ({len(results)} found)",
            show_header=True,
            header_style="bold magenta",
            border_style="blue"
        )
        table.add_column("Rank", style="cyan", width=6, justify="center")
        table.add_column("Score", justify="right", width=10)
        table.add_column("Source", style="green", width=30)
        table.add_column("Text Preview", width=80)
        
        for idx, result in enumerate(results, 1):
            score = result.get('_score', 0)
            source = result.get('_source', {})
            text = source.get('text', 'N/A')
            filename = source.get('metadata', {}).get('filename', 'Unknown')
            
            # Truncate text for display
            text_preview = text[:150] + "..." if len(text) > 150 else text
            
            table.add_row(
                str(idx),
                f"{score:.4f}",
                filename[:28],
                text_preview
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise click.Abort()
