# 🚀 Quick Reference: Streamlit to CLI Conversion

## 📌 Common Conversions Cheat Sheet

### User Input

| Streamlit | CLI (Click) | Example |
|-----------|-------------|---------|
| `st.text_input("Query")` | `@click.argument('query')` | `rag search <query>` |
| `st.file_uploader("File")` | `@click.argument('file', type=click.Path())` | `rag ingest file.pdf` |
| `st.selectbox(["A","B"])` | `@click.option('--type', type=click.Choice(['A','B']))` | `rag --type A` |
| `st.slider("K", 1, 10)` | `@click.option('--k', type=int, default=5)` | `rag --k 5` |
| `st.checkbox("Enable")` | `@click.option('--enable', is_flag=True)` | `rag --enable` |
| `st.button("Submit")` | Command execution | `rag command` |

### Output/Display

| Streamlit | CLI (Rich) | Code |
|-----------|------------|------|
| `st.write("Text")` | `console.print("Text")` | `from rich.console import Console` |
| `st.success("Done")` | `console.print("[green]Done[/green]")` | Rich markup |
| `st.error("Error")` | `console.print("[red]Error[/red]")` | Rich markup |
| `st.warning("Warn")` | `console.print("[yellow]Warn[/yellow]")` | Rich markup |
| `st.markdown(md)` | `console.print(Markdown(md))` | `from rich.markdown import Markdown` |
| `st.table(df)` | `console.print(Table(...))` | `from rich.table import Table` |
| `st.progress(0.5)` | `Progress(...)` | `from rich.progress import Progress` |

### State Management

| Streamlit | CLI Alternative |
|-----------|-----------------|
| `st.session_state.key` | Config file (.env, YAML) |
| `st.session_state.history` | SQLite database |
| `st.cache_data` | File cache or Redis |
| `st.cache_resource` | Singleton pattern |

---

## 🔧 Code Templates

### Basic CLI Command

```python
import click
from rich.console import Console

console = Console()

@click.command()
@click.argument('query')
@click.option('--top-k', default=5, help='Number of results')
def search(query, top_k):
    """Search for documents."""
    console.print(f"Searching for: {query}")
    # Your logic here
    console.print("[green]Done![/green]")
```

### Command with File Input

```python
@click.command()
@click.argument('filepath', type=click.Path(exists=True))
@click.option('--recursive', is_flag=True)
def ingest(filepath, recursive):
    """Ingest documents."""
    path = Path(filepath)
    
    if path.is_file():
        process_file(path)
    elif path.is_dir() and recursive:
        for file in path.rglob('*.pdf'):
            process_file(file)
```

### Progress Bar

```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Processing...", total=len(files))
    
    for file in files:
        process(file)
        progress.advance(task)
```

### Table Output

```python
from rich.table import Table

table = Table(title="Results")
table.add_column("#", style="cyan")
table.add_column("Score", style="yellow")
table.add_column("Text")

for i, result in enumerate(results):
    table.add_row(str(i+1), f"{result['score']:.3f}", result['text'])

console.print(table)
```

### Error Handling

```python
@click.command()
def mycommand():
    """My command."""
    try:
        # Your code
        result = do_something()
        console.print("[green]Success![/green]")
    except FileNotFoundError:
        console.print("[red]Error: File not found[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise
```

---

## 📁 Project Structure

```
local-rag-cli/
├── .env                      # Configuration (user-specific)
├── .env.example              # Configuration template
├── requirements.txt          # Python dependencies
├── setup.py                  # Package installation
├── README.md                 # Documentation
│
├── config/
│   ├── __init__.py
│   └── settings.py          # Pydantic settings
│
├── src/
│   ├── __init__.py
│   ├── cli.py               # Main CLI entry point
│   │
│   ├── commands/            # CLI command groups
│   │   ├── __init__.py
│   │   ├── ingest.py       # Document ingestion
│   │   ├── search.py       # Search commands
│   │   ├── config.py       # Config commands
│   │   └── index.py        # Index management
│   │
│   ├── core/                # Business logic (from original src/)
│   │   ├── __init__.py
│   │   ├── document_processor.py  # PDF, DOCX processing
│   │   ├── embeddings.py          # Embedding generation
│   │   ├── opensearch_client.py   # OpenSearch ops
│   │   ├── search.py              # Search logic
│   │   └── rag.py                 # RAG pipeline
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py        # Logging setup
│       └── helpers.py       # Utility functions
│
└── tests/
    ├── __init__.py
    ├── test_cli.py
    ├── test_ingest.py
    └── test_search.py
```

---

## 🎯 Implementation Order

### Phase 1: Foundation (Day 1-2)
1. ✅ Create directory structure
2. ✅ Set up `requirements.txt`
3. ✅ Create `config/settings.py`
4. ✅ Create basic `cli.py` with Click

### Phase 2: Core Logic (Day 3-5)
1. ✅ Copy and adapt `src/embeddings.py`
2. ✅ Copy and adapt `src/opensearch_utils.py` → `opensearch_client.py`
3. ✅ Copy and adapt `src/ocr.py` → `document_processor.py`
4. ✅ Create `rag.py` from chat logic

### Phase 3: CLI Commands (Day 6-8)
1. ✅ `rag config init/show/test`
2. ✅ `rag index create/list/delete`
3. ✅ `rag ingest <file>`
4. ✅ `rag search <query>`
5. ✅ `rag ask <question>`

### Phase 4: Polish (Day 9-10)
1. ✅ Add progress bars
2. ✅ Add beautiful output
3. ✅ Add error handling
4. ✅ Write documentation

---

## 🔍 Debugging Checklist

### Command Not Working?
- [ ] Check imports
- [ ] Check file permissions
- [ ] Check environment variables (.env loaded?)
- [ ] Check OpenSearch is running
- [ ] Check logs

### OpenSearch Issues?
```bash
# Check if running
curl http://localhost:9200

# Check index exists
curl http://localhost:9200/_cat/indices

# Delete and recreate
curl -X DELETE http://localhost:9200/documents
```

### Import Errors?
```bash
# Check package installed
pip list | grep <package>

# Reinstall
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Essential Commands

### Development

```bash
# Install in development mode
pip install -e .

# Run CLI
python -m src.cli

# Or if installed
rag --help

# Run with Python debugger
python -m pdb src/cli.py search "test"
```

### Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_cli.py::test_search

# With coverage
pytest --cov=src tests/
```

### Formatting

```bash
# Format code
black src/

# Check types
mypy src/

# Lint
flake8 src/
```

---

## 💡 Pro Tips

### 1. Development Workflow
```bash
# Terminal 1: OpenSearch
docker run -p 9200:9200 opensearchproject/opensearch:latest

# Terminal 2: Development
python src/cli.py search "test"

# Terminal 3: Logs
tail -f logs/rag.log
```

### 2. Quick Testing
```python
# Create test script: test_quick.py
from src.core.search import SearchEngine

engine = SearchEngine()
results = engine.search("test")
print(results)
```

### 3. Environment Management
```bash
# Create .env from example
cp .env.example .env

# Load in Python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🆘 Common Errors & Solutions

### Error: "OpenSearch connection refused"
**Solution:**
```bash
# Start OpenSearch
docker-compose up -d opensearch
# Or
docker run -p 9200:9200 opensearchproject/opensearch:latest
```

### Error: "Module not found"
**Solution:**
```bash
# Install package
pip install -e .
# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Error: "Click command not found"
**Solution:**
```bash
# Check entry point in setup.py
entry_points={
    'console_scripts': [
        'rag=src.cli:cli',
    ],
}

# Reinstall
pip install -e .
```

---

## 📖 Resources

### Documentation
- Click: https://click.palletsprojects.com/
- Rich: https://rich.readthedocs.io/
- Pydantic: https://docs.pydantic.dev/
- OpenSearch: https://opensearch.org/docs/

### Examples
- Click examples: https://github.com/pallets/click/tree/main/examples
- Rich examples: https://github.com/Textualize/rich/tree/master/examples

---

## ✅ Daily Checklist

### Before Starting
- [ ] OpenSearch running
- [ ] Virtual environment activated
- [ ] .env file configured

### After Each Session
- [ ] Commit code
- [ ] Update documentation
- [ ] Test command works
- [ ] Check for errors in logs

---

Keep this reference handy! 📌