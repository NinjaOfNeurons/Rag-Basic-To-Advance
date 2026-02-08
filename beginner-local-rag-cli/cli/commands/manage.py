import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from opensearchpy import OpenSearch
from src.ingestion import delete_index, delete_documents_by_document_name

console = Console()

# Default values (will be overridden by constants if available)
try:
    from src.constants import OPENSEARCH_HOST, OPENSEARCH_PORT
except ImportError:
    OPENSEARCH_HOST = 'localhost'
    OPENSEARCH_PORT = 9200

# Try to get INDEX_NAME, use default if not available
try:
    from src.constants import INDEX_NAME
except ImportError:
    INDEX_NAME = 'rag_index'

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

@click.group()
def manage():
    """Manage the RAG system."""
    pass

@manage.command()
def status():
    """Check system status."""
    
    console.print(Panel.fit("[bold]System Status Check[/bold]", border_style="cyan"))
    
    # Check OpenSearch
    try:
        client = OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )
        info = client.info()
        console.print("[green]✓[/green] OpenSearch: [bold]Connected[/bold]")
        console.print(f"  Version: {info.get('version', {}).get('number', 'unknown')}")
        console.print(f"  Cluster: {info.get('cluster_name', 'unknown')}")
    except Exception as e:
        console.print("[red]✗[/red] OpenSearch: [bold]Disconnected[/bold]")
        console.print(f"  Error: {str(e)}")
    
    # Check Ollama
    if OLLAMA_AVAILABLE:
        try:
            import ollama
            models = ollama.list()
            console.print(f"\n[green]✓[/green] Ollama: [bold]Available[/bold]")
            model_list = models.get('models', [])
            console.print(f"  Models installed: {len(model_list)}")
            if model_list:
                for model in model_list[:3]:  # Show first 3
                    console.print(f"    • {model.get('name', 'unknown')}")
        except Exception as e:
            console.print(f"\n[red]✗[/red] Ollama: [bold]Unavailable[/bold]")
            console.print(f"  Error: {str(e)}")
    else:
        console.print(f"\n[yellow]⚠[/yellow] Ollama: [bold]Not installed[/bold]")
    
    # Check Embedding Model
    try:
        from src.embeddings import get_embedding_model
        model = get_embedding_model()
        console.print(f"\n[green]✓[/green] Embedding Model: [bold]Loaded[/bold]")
    except Exception as e:
        console.print(f"\n[red]✗[/red] Embedding Model: [bold]Failed[/bold]")
        console.print(f"  Error: {str(e)}")
    
    # Check uploaded files
    upload_dir = project_root / "uploaded_files"
    if upload_dir.exists():
        files = list(upload_dir.glob("*.pdf"))
        console.print(f"\n[cyan]ℹ[/cyan] Uploaded Files: {len(files)}")
        if files:
            for f in files[:5]:  # Show first 5
                console.print(f"    • {f.name}")

@manage.command()
@click.option('--index-name', default=INDEX_NAME, help='OpenSearch index name')
def list_indices(index_name):
    """List OpenSearch indices and their stats."""
    try:
        client = OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
        )
        
        # Get all indices
        indices = client.cat.indices(format='json')
        
        table = Table(title="OpenSearch Indices", border_style="blue")
        table.add_column("Index Name", style="cyan")
        table.add_column("Docs", justify="right", style="green")
        table.add_column("Size", justify="right")
        table.add_column("Health", justify="center")
        
        for idx in indices:
            health_color = "green" if idx['health'] == 'green' else "yellow" if idx['health'] == 'yellow' else "red"
            table.add_row(
                idx['index'],
                idx.get('docs.count', '0'),
                idx.get('store.size', 'N/A'),
                f"[{health_color}]{idx['health']}[/{health_color}]"
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@manage.command()
@click.confirmation_option(prompt='Are you sure you want to delete the entire index?')
def delete_idx():
    """Delete the OpenSearch index (removes all documents)."""
    try:
        client = OpenSearch(
            hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
            http_compress=True,
            use_ssl=False,
            verify_certs=False,
        )
        
        delete_index(client)
        console.print(f"[green]✓ Index '{INDEX_NAME}' deleted successfully[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@manage.command()
@click.argument('document_name')
@click.confirmation_option(prompt='Are you sure you want to delete this document?')
def delete_doc(document_name):
    """Delete a specific document by filename."""
    try:
        result = delete_documents_by_document_name(document_name)
        
        deleted = result.get('deleted', 0)
        if deleted > 0:
            console.print(f"[green]✓ Deleted {deleted} chunks from document '{document_name}'[/green]")
        else:
            console.print(f"[yellow]No documents found with name '{document_name}'[/yellow]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")

@manage.command()
def list_docs():
    """List all uploaded documents."""
    upload_dir = project_root / "uploaded_files"
    
    if not upload_dir.exists():
        console.print("[yellow]No uploaded_files directory found[/yellow]")
        return
    
    files = sorted(upload_dir.glob("*.pdf"))
    
    if not files:
        console.print("[yellow]No documents found[/yellow]")
        return
    
    table = Table(title=f"Uploaded Documents ({len(files)})", border_style="cyan")
    table.add_column("#", style="dim", width=4)
    table.add_column("Filename", style="cyan")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Modified", style="yellow")
    
    for i, file in enumerate(files, 1):
        import os
        from datetime import datetime
        
        size_mb = file.stat().st_size / (1024 * 1024)
        mod_time = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
        
        table.add_row(
            str(i),
            file.name,
            f"{size_mb:.2f} MB",
            mod_time
        )
    
    console.print(table)
