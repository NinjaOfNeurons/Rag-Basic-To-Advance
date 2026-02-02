# Local RAG System - CLI Conversion Plan

## Project Overview
Converting the Streamlit-based local RAG system to a command-line interface (CLI) version.

**Original Stack:**
- Streamlit (Web UI)
- OpenSearch (Vector Database)
- Sentence Transformers (Embeddings)
- PyTesseract (OCR)
- Local LLMs

**CLI Architecture:**
- Click/Typer for CLI framework
- Same backend (OpenSearch, embeddings, LLM)
- Rich for beautiful terminal output
- Progress bars for long operations

## Directory Structure

```
local-rag-cli/
├── README.md
├── requirements.txt
├── setup.py
├── .env.example
├── config/
│   └── settings.py          # Configuration management
├── src/
│   ├── __init__.py
│   ├── cli.py              # Main CLI entry point
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── ingest.py       # Document ingestion commands
│   │   ├── query.py        # Search/query commands
│   │   ├── manage.py       # Index management commands
│   │   └── config.py       # Configuration commands
│   ├── core/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   ├── embeddings.py
│   │   ├── search.py
│   │   ├── llm.py
│   │   └── opensearch_client.py
│   └── utils/
│       ├── __init__.py
│       ├── logger.py
│       └── helpers.py
└── tests/
    └── ...
```

## CLI Commands Structure

### 1. Document Ingestion
```bash
rag ingest <file_or_directory>
rag ingest --path ./docs --recursive
rag ingest --url https://example.com/doc.pdf
rag batch-ingest --file-list documents.txt
```

### 2. Search/Query
```bash
rag search "query text"
rag search "query" --top-k 10
rag search "query" --hybrid  # Hybrid search
rag ask "question"           # RAG with LLM response
rag ask "question" --stream  # Streaming response
```

### 3. Index Management
```bash
rag index create --name my_index
rag index list
rag index delete --name my_index
rag index stats --name my_index
rag index reset
```

### 4. Configuration
```bash
rag config init              # Initialize configuration
rag config show              # Show current config
rag config set embedding-model <model_name>
rag config set opensearch-host localhost:9200
rag config test              # Test connections
```

### 5. Interactive Mode
```bash
rag interactive              # Start interactive REPL
rag chat                     # Chat mode with context
```

## Key Features to Implement

### Phase 1: Core Functionality
- [x] CLI framework setup (Click/Typer)
- [ ] Configuration management
- [ ] OpenSearch client
- [ ] Document processing (PDF, DOCX, TXT)
- [ ] Embedding generation
- [ ] Basic search functionality

### Phase 2: Advanced Features
- [ ] Hybrid search (BM25 + semantic)
- [ ] LLM integration (Ollama/local models)
- [ ] RAG pipeline
- [ ] Batch processing
- [ ] Progress indicators

### Phase 3: User Experience
- [ ] Interactive mode/REPL
- [ ] Beautiful terminal output (Rich)
- [ ] Error handling and validation
- [ ] Logging and debugging
- [ ] Help documentation

### Phase 4: Additional Features
- [ ] Export results (JSON, CSV, MD)
- [ ] Document metadata management
- [ ] Query history
- [ ] Configuration profiles
- [ ] Performance metrics

## Implementation Steps

1. **Setup Base CLI Structure**
   - Install dependencies (Click/Typer, Rich)
   - Create main entry point
   - Setup command groups

2. **Configuration System**
   - Environment variables
   - Config file (.ragrc or config.yaml)
   - CLI config commands

3. **Core Components**
   - Port existing modules from src/
   - Adapt for CLI usage
   - Remove Streamlit dependencies

4. **Commands Implementation**
   - Implement each command group
   - Add progress bars and status updates
   - Input validation

5. **Testing & Documentation**
   - Unit tests
   - Integration tests
   - README with examples
   - Man-style help pages

## Dependencies

```
# Core
click>=8.0.0  # or typer>=0.9.0
rich>=13.0.0
python-dotenv>=1.0.0

# Document Processing
PyPDF2>=3.0.0
python-docx>=1.0.0
pytesseract>=0.3.0

# ML/Search
sentence-transformers>=2.2.0
opensearch-py>=2.0.0

# LLM
ollama>=0.1.0  # or other local LLM client

# Utils
pydantic>=2.0.0
loguru>=0.7.0
```

## Configuration File Example

```yaml
# .ragrc or config/settings.yaml
opensearch:
  host: localhost
  port: 9200
  index: documents
  
embeddings:
  model_path: ./embedding_model/
  model_name: all-mpnet-base-v2
  
llm:
  provider: ollama
  model: llama3.2
  temperature: 0.7
  
search:
  default_top_k: 5
  hybrid_weight: 0.5
  
processing:
  chunk_size: 500
  chunk_overlap: 50
```

## Example Usage Scenarios

### Scenario 1: First-time Setup
```bash
# Initialize configuration
rag config init

# Test connections
rag config test

# Create index
rag index create --name my_docs

# Ingest documents
rag ingest ./my_documents/ --recursive
```

### Scenario 2: Daily Usage
```bash
# Add new document
rag ingest report.pdf

# Search
rag search "machine learning best practices"

# Ask question with RAG
rag ask "What are the key findings in the Q4 report?"
```

### Scenario 3: Batch Operations
```bash
# Batch ingest from file list
rag batch-ingest --file-list docs.txt --parallel 4

# Export search results
rag search "query" --export results.json
```

## Migration Notes

- Streamlit session state → CLI state management (config files)
- st.file_uploader → File path arguments
- st.text_input → CLI arguments/prompts
- st.progress → Rich progress bars
- st.write/st.markdown → Rich console output
- Callbacks → Click callbacks or progress hooks

## Success Criteria

- [ ] All core Streamlit features available in CLI
- [ ] Fast startup time (< 2 seconds)
- [ ] Clear, helpful error messages
- [ ] Comprehensive documentation
- [ ] Cross-platform compatibility
- [ ] Easy installation (pip install)