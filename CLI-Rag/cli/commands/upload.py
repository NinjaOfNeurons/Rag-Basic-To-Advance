import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from pathlib import Path
import sys
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

console = Console()

# Try to import constants, use defaults if not available
try:
    from src.constants import OPENSEARCH_HOST, OPENSEARCH_PORT
except ImportError:
    OPENSEARCH_HOST = 'localhost'
    OPENSEARCH_PORT = 9200

try:
    from src.constants import CHUNK_SIZE, CHUNK_OVERLAP
except ImportError:
    CHUNK_SIZE = 512
    CHUNK_OVERLAP = 50

@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--index-name', default='rag_index', help='OpenSearch index name')
def upload(filepath, index_name):
    """Upload and process a PDF document."""
    
    filepath = Path(filepath)
    
    if not filepath.suffix.lower() == '.pdf':
        console.print("[red]Error: Only PDF files are supported[/red]")
        raise click.Abort()
    
    console.print(f"[bold blue]Processing document:[/bold blue] {filepath.name}\n")
    
    try:
        # Import required functions
        from src.ocr import extract_text_from_pdf
        from src.embeddings import get_embedding_model, generate_embeddings
        from src.ingestion import create_index, bulk_index_documents
        from opensearchpy import OpenSearch
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
            transient=False
        ) as progress:
            
            # Step 1: Copy file to uploaded_files directory
            task1 = progress.add_task("Copying file...", total=None)
            upload_dir = project_root / "uploaded_files"
            upload_dir.mkdir(exist_ok=True)
            dest_path = upload_dir / filepath.name
            shutil.copy2(filepath, dest_path)
            progress.update(task1, completed=True)
            console.print(f"[green]✓[/green] File copied to uploaded_files/")
            
            # Step 2: Extract text from PDF
            task2 = progress.add_task("Extracting text from PDF...", total=None)
            full_text = extract_text_from_pdf(str(dest_path))
            progress.update(task2, completed=True)
            console.print(f"[green]✓[/green] Extracted {len(full_text)} characters")
            
            # Step 3: Chunk the text
            task3 = progress.add_task("Chunking text...", total=None)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CHUNK_SIZE,
                chunk_overlap=CHUNK_OVERLAP,
                length_function=len,
            )
            chunks = text_splitter.split_text(full_text)
            progress.update(task3, completed=True)
            console.print(f"[green]✓[/green] Created {len(chunks)} chunks")
            
            # Step 4: Load embedding model
            task4 = progress.add_task("Loading embedding model...", total=None)
            embedding_model = get_embedding_model()
            progress.update(task4, completed=True)
            console.print(f"[green]✓[/green] Embedding model loaded")
            
            # Step 5: Generate embeddings
            task5 = progress.add_task("Generating embeddings...", total=None)
            embeddings = generate_embeddings(chunks)
            progress.update(task5, completed=True)
            console.print(f"[green]✓[/green] Generated {len(embeddings)} embeddings")
            
            # Step 6: Prepare documents for indexing
            task6 = progress.add_task("Preparing documents...", total=None)
            documents = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                doc = {
                    'text': chunk,
                    'embedding': embedding.tolist(),
                    'metadata': {
                        'filename': filepath.name,
                        'chunk_id': i,
                        'total_chunks': len(chunks),
                        'source': str(dest_path)
                    }
                }
                documents.append(doc)
            progress.update(task6, completed=True)
            console.print(f"[green]✓[/green] Prepared {len(documents)} documents")
            
            # Step 7: Create OpenSearch client and index
            task7 = progress.add_task("Creating index if needed...", total=None)
            client = OpenSearch(
                hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
                http_compress=True,
                use_ssl=False,
                verify_certs=False,
                ssl_assert_hostname=False,
                ssl_show_warn=False,
            )
            
            # Check if index exists, if not create it
            if not client.indices.exists(index=index_name):
                create_index(client)
                console.print(f"[green]✓[/green] Created index: {index_name}")
            else:
                console.print(f"[green]✓[/green] Using existing index: {index_name}")
            progress.update(task7, completed=True)
            
            # Step 8: Bulk index documents
            task8 = progress.add_task(f"Indexing {len(documents)} documents...", total=None)
            success_count, errors = bulk_index_documents(documents)
            progress.update(task8, completed=True)
            
            if errors:
                console.print(f"[yellow]⚠[/yellow] Indexed with some errors: {success_count}/{len(documents)} successful")
                console.print(f"[dim]Errors: {len(errors)}[/dim]")
            else:
                console.print(f"[green]✓[/green] Successfully indexed all {success_count} documents")
        
        console.print(f"\n[bold green]✅ Upload Complete![/bold green]")
        console.print(f"[cyan]Document:[/cyan] {filepath.name}")
        console.print(f"[cyan]Index:[/cyan] {index_name}")
        console.print(f"[cyan]Chunks:[/cyan] {len(chunks)}")
        console.print(f"[cyan]Location:[/cyan] uploaded_files/{filepath.name}")
        
    except ImportError as e:
        console.print(f"[bold red]Import Error:[/bold red] {str(e)}")
        console.print("\n[yellow]Missing dependency. Please check your installation.[/yellow]")
        raise click.Abort()
    except Exception as e:
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise click.Abort()
