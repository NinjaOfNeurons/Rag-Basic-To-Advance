# 📚 Step-by-Step Guide: Converting Streamlit RAG to CLI

## 🎯 Goal
Transform the Streamlit-based local RAG system into a professional CLI tool while **understanding every component**.

## 📋 Prerequisites
- ✅ You have cloned the original repo: `git clone https://github.com/jamwithai/local-rag-system.git`
- ✅ Python 3.9+ installed
- ✅ Basic understanding of the original app

---

## 🗺️ The Learning Journey

### Phase 1: Understanding the Original Architecture (Week 1)
**Goal**: Map out what we're converting

#### Step 1.1: Explore the Original Structure
```bash
cd local-rag-system
tree -L 2  # or use 'ls -R' if tree not available
```

**Key Files to Examine:**
```
local-rag-system/
├── Welcome.py              ← Main Streamlit entry point
├── pages/                  ← Streamlit pages (multi-page app)
│   └── chat.py            ← The chat interface
├── src/                    ← Core logic (THIS is what we'll reuse!)
│   ├── constants.py       ← Configuration
│   ├── embeddings.py      ← Embedding generation
│   ├── ocr.py            ← OCR for PDFs
│   ├── opensearch_utils.py ← OpenSearch operations
│   └── chat.py           ← RAG logic
├── requirements.txt       ← Dependencies
└── notebooks/            ← Learning materials
```

**🎓 Learning Task 1:**
1. Read `src/constants.py` - understand all configuration options
2. Open `Welcome.py` - see how Streamlit initializes
3. Open `pages/chat.py` - understand the user flow

**📝 What to Document:**
- What does each file in `src/` do?
- Which parts are Streamlit-specific (UI)?
- Which parts are reusable (business logic)?

---

### Phase 2: Setting Up the CLI Foundation (Week 1-2)
**Goal**: Create the CLI skeleton

#### Step 2.1: Understand CLI Design Patterns
Before coding, let's understand how professional CLIs work:

**Examples of Good CLIs:**
- `git` - git clone, git add, git commit
- `docker` - docker run, docker build, docker ps
- `aws` - aws s3 ls, aws ec2 describe-instances

**Our CLI Structure:**
```bash
rag config init              # Setup
rag ingest document.pdf      # Add documents
rag search "my query"        # Search
rag ask "question?"          # RAG query
rag index create             # Index management
```

#### Step 2.2: Choose a CLI Framework
We'll use **Click** (most popular) or **Typer** (modern, type-safe)

**Why Click?**
- Industry standard (used by Flask, AWS CLI)
- Great documentation
- Rich ecosystem

**Installation:**
```bash
pip install click rich python-dotenv
```

#### Step 2.3: Create Your First CLI Command
Create `cli_test.py`:
```python
import click

@click.group()
def cli():
    """My first CLI!"""
    pass

@cli.command()
@click.argument('name')
def hello(name):
    """Say hello to someone."""
    click.echo(f'Hello {name}!')

if __name__ == '__main__':
    cli()
```

**Test it:**
```bash
python cli_test.py hello World
# Output: Hello World!
```

**🎓 Learning Task 2:**
1. Create 3 simple CLI commands
2. Add options with `@click.option()`
3. Try command groups with `@click.group()`

---

### Phase 3: Mapping Streamlit → CLI (Week 2)
**Goal**: Plan the conversion

#### Step 3.1: Understand Streamlit Components
Let's break down what Streamlit does:

**Streamlit UI Component** → **CLI Equivalent**

| Streamlit | CLI Alternative | Example |
|-----------|----------------|---------|
| `st.file_uploader()` | `click.argument('file')` | `rag ingest file.pdf` |
| `st.text_input()` | `click.argument()` or `click.option()` | `rag search "query"` |
| `st.button()` | Command execution | `rag ask` |
| `st.write()` / `st.markdown()` | `console.print()` (Rich) | Formatted output |
| `st.progress()` | Progress bar (Rich) | Loading indicators |
| `st.session_state` | Config files / database | Persistent storage |
| `st.sidebar` | CLI options | `--option value` |

#### Step 3.2: Create Conversion Map
Create a document mapping each Streamlit feature:

**Example from Welcome.py:**
```python
# Streamlit version:
if st.button("Initialize System"):
    setup_opensearch()
    st.success("System initialized!")

# CLI version:
@cli.command()
def init():
    """Initialize the RAG system."""
    setup_opensearch()
    console.print("[green]✓ System initialized![/green]")
```

**🎓 Learning Task 3:**
1. Open `pages/chat.py`
2. List all Streamlit components (st.*)
3. Map each to CLI equivalent
4. Identify which logic can be reused from `src/`

---

### Phase 4: Extracting Reusable Logic (Week 2-3)
**Goal**: Separate UI from business logic

#### Step 4.1: Understand the Original Architecture

**Current (Streamlit):**
```
Welcome.py (UI + Logic mixed)
    ↓
Uses src/embeddings.py, src/opensearch_utils.py
    ↓
Streamlit handles: file upload, display, state
```

**Target (CLI):**
```
cli.py (UI - Click commands)
    ↓
core/ modules (Business logic - reused from src/)
    ↓
CLI handles: arguments, output formatting
```

#### Step 4.2: Create the Core Modules
Let's reorganize:

**New Structure:**
```
local-rag-cli/
├── src/
│   ├── cli.py              ← CLI commands (NEW)
│   ├── core/               ← Reusable logic (from original src/)
│   │   ├── embeddings.py   ← COPY from original
│   │   ├── opensearch_client.py  ← COPY & ADAPT
│   │   ├── document_processor.py ← COPY & RENAME
│   │   └── rag.py          ← COPY chat logic
│   └── utils/
│       └── logger.py       ← NEW - for CLI logging
└── config/
    └── settings.py         ← NEW - replaces constants.py
```

**🎓 Learning Task 4:**
1. Copy `src/` from original to your new project
2. Identify which files are pure logic (no Streamlit)
3. Create a checklist of files that need modification

---

### Phase 5: Building Core Components (Week 3-4)
**Goal**: Create the foundation modules

#### Step 5.1: Configuration Management
**Original:**
```python
# constants.py
OPENSEARCH_HOST = "localhost"
EMBEDDING_MODEL_PATH = "./embedding_model/"
```

**CLI Version (Better):**
```python
# config/settings.py using Pydantic
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    opensearch_host: str = "localhost"
    opensearch_port: int = 9200
    embedding_model_path: str = "./embedding_model/"
    
    class Config:
        env_file = ".env"
```

**Why Better?**
- Environment variables support
- Type validation
- Easy to override
- Production-ready

#### Step 5.2: Document Processing
**Task**: Convert the file upload logic to file path processing

**Original (Streamlit):**
```python
uploaded_file = st.file_uploader("Upload PDF")
if uploaded_file:
    bytes_data = uploaded_file.read()
    process_pdf(bytes_data)
```

**CLI Version:**
```python
@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def ingest(filepath):
    """Ingest a document."""
    with open(filepath, 'rb') as f:
        process_pdf(f.read())
```

**🎓 Learning Task 5:**
1. Study `src/ocr.py` from original
2. Understand how PDFs are processed
3. Modify to accept file paths instead of uploaded files

---

### Phase 6: Implementing CLI Commands (Week 4-5)
**Goal**: Build actual commands

#### Step 6.1: Command Categories
Let's organize commands into groups:

**1. Configuration Commands**
```bash
rag config init        # Create .env file
rag config show        # Display current config
rag config test        # Test connections
```

**2. Index Management**
```bash
rag index create       # Create new index
rag index list         # List all indexes
rag index delete NAME  # Delete index
rag index stats        # Show statistics
```

**3. Document Commands**
```bash
rag ingest FILE               # Ingest single file
rag ingest DIRECTORY --recursive  # Ingest folder
rag batch-ingest FILE_LIST    # Batch ingest
```

**4. Query Commands**
```bash
rag search "query"            # Search only
rag ask "question"            # RAG with LLM
rag interactive               # Interactive mode
```

#### Step 6.2: Example Implementation
Let's build the `search` command together:

```python
# src/cli.py
import click
from rich.console import Console
from rich.table import Table
from src.core.search import SearchEngine

console = Console()

@cli.command()
@click.argument('query')
@click.option('--top-k', default=5, help='Number of results')
def search(query, top_k):
    """Search for documents."""
    console.print(f"[cyan]Searching for: {query}[/cyan]\n")
    
    # Use existing search logic
    search_engine = SearchEngine()
    results = search_engine.search(query, top_k=top_k)
    
    # Format output
    table = Table(title="Search Results")
    table.add_column("#", style="cyan")
    table.add_column("Score", style="yellow")
    table.add_column("Text", style="white")
    
    for i, result in enumerate(results, 1):
        table.add_row(
            str(i),
            f"{result['score']:.3f}",
            result['text'][:100] + "..."
        )
    
    console.print(table)
```

**🎓 Learning Task 6:**
1. Implement `rag config show` command
2. Add error handling
3. Add beautiful output with Rich library

---

### Phase 7: Adding Advanced Features (Week 5-6)
**Goal**: Polish and add extras

#### Step 7.1: Interactive Mode (REPL)
Create a chat-like experience:

```python
@cli.command()
def interactive():
    """Start interactive mode."""
    console.print("[bold]RAG Interactive Mode[/bold]")
    console.print("Type 'exit' to quit\n")
    
    while True:
        query = console.input("[green]You:[/green] ")
        
        if query.lower() == 'exit':
            break
            
        # Process query
        answer = rag_pipeline.ask(query)
        console.print(f"[cyan]Assistant:[/cyan] {answer}\n")
```

#### Step 7.2: Progress Indicators
```python
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("Processing...", total=100)
    
    for i in range(100):
        # Do work
        progress.update(task, advance=1)
```

#### Step 7.3: Output Formatting
```python
from rich.panel import Panel
from rich.markdown import Markdown

# Display answer in a nice panel
answer = "Your answer here..."
console.print(Panel(Markdown(answer), title="Answer"))
```

**🎓 Learning Task 7:**
1. Add streaming responses for `ask` command
2. Add export functionality (JSON, CSV)
3. Add query history

---

### Phase 8: Testing & Documentation (Week 6)
**Goal**: Make it production-ready

#### Step 8.1: Testing
```bash
# Manual testing
rag config init
rag index create
rag ingest test.pdf
rag search "test query"
rag ask "what is this about?"
```

#### Step 8.2: Documentation
Create comprehensive README:
- Installation instructions
- Configuration guide
- Command reference
- Examples
- Troubleshooting

**🎓 Learning Task 8:**
1. Create test files
2. Write user documentation
3. Add help messages to all commands

---

## 🎯 Milestone Checklist

### Week 1-2: Foundation
- [ ] Understand original structure
- [ ] Set up development environment
- [ ] Create basic CLI skeleton
- [ ] Map Streamlit → CLI conversions

### Week 3-4: Core Implementation
- [ ] Copy and adapt core modules
- [ ] Implement configuration system
- [ ] Build document processing
- [ ] Create OpenSearch client

### Week 5-6: Commands
- [ ] Config commands (init, show, test)
- [ ] Index commands (create, list, delete)
- [ ] Ingest command
- [ ] Search command
- [ ] Ask command (RAG)
- [ ] Interactive mode

### Week 6-7: Polish
- [ ] Add progress indicators
- [ ] Beautiful output formatting
- [ ] Error handling
- [ ] Documentation
- [ ] Testing

---

## 📚 Learning Resources

### Click Documentation
- Official Docs: https://click.palletsprojects.com/
- Tutorial: https://click.palletsprojects.com/en/8.1.x/quickstart/

### Rich (Beautiful Terminal Output)
- GitHub: https://github.com/Textualize/rich
- Examples: https://rich.readthedocs.io/

### Pydantic Settings
- Docs: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

---

## 💡 Key Concepts to Master

1. **Separation of Concerns**
   - UI (CLI commands) vs Logic (core modules)
   
2. **Configuration Management**
   - Environment variables
   - Config files
   - Defaults

3. **Error Handling**
   - Graceful failures
   - Helpful error messages

4. **User Experience**
   - Progress indicators
   - Clear output
   - Interactive help

---

## 🚀 Next Steps

Ready to start? Here's your first homework:

1. **Today**: Explore the original repo, document what you find
2. **Tomorrow**: Set up a new project, create first CLI command
3. **This Week**: Complete Phase 1 & 2
4. **Next Week**: Start Phase 3 & 4

---

## ❓ Questions to Answer as You Go

1. What does each file in `src/` do?
2. How does OpenSearch integration work?
3. How are embeddings generated?
4. How does the RAG pipeline work?
5. What are the main pain points in the Streamlit version?
6. How can CLI improve the workflow?

---

## 📝 Pro Tips

- **Don't rush**: Understanding > Speed
- **Document everything**: Future you will thank you
- **Test frequently**: After each small change
- **Ask questions**: Create issues, take notes
- **Version control**: Commit often with clear messages

---

Ready to begin? Let's start with **Phase 1: Understanding the Original Architecture**!

Would you like me to help you create a detailed exploration guide for the original codebase?