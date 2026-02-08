# 📚 Local RAG System - CLI Version

A privacy-friendly, command-line interface for building and querying a Retrieval-Augmented Generation (RAG) system using local LLMs. Process your personal documents, search through them semantically, and chat with your data - all running locally on your machine.

![CLI Demo](https://img.shields.io/badge/CLI-Powered-blue?style=for-the-badge&logo=gnubash)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

---

## 🌟 Features

- **📄 PDF Processing**: Upload and process PDF documents with OCR support
- **🔍 Hybrid Search**: Combine semantic and keyword-based search for best results
- **💬 Interactive Chat**: Chat with your documents using local LLMs (Ollama)
- **🎨 Beautiful CLI**: Rich terminal output with progress bars and formatting
- **🔒 Privacy-First**: Everything runs locally - no cloud services required
- **⚡ Fast**: Powered by OpenSearch for lightning-fast vector similarity search

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Commands Reference](#commands-reference)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Prerequisites

Before installing, ensure you have the following installed:

### Required Services

1. **Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **OpenSearch** (Vector Database)
   
   **Option A: Docker (Recommended)**
   ```bash
   docker run -d \
     -p 9200:9200 \
     -p 9600:9600 \
     -e "discovery.type=single-node" \
     -e "plugins.security.disabled=true" \
     --name opensearch-node \
     opensearchproject/opensearch:latest
   ```

   **Option B: Manual Installation**
   - Download from [OpenSearch Downloads](https://opensearch.org/downloads.html)
   - Follow installation guide for your OS

   **Verify OpenSearch is running:**
   ```bash
   curl -X GET "localhost:9200"
   ```

3. **Ollama** (Local LLM Runtime)
   
   **Linux/Mac:**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```

   **Windows:**
   - Download installer from [ollama.com](https://ollama.com)

   **Pull the required model:**
   ```bash
   ollama pull llama3.2:1b
   # OR for better quality (requires more RAM)
   ollama pull llama2
   ```

   **Verify Ollama:**
   ```bash
   ollama list
   ```

### Optional but Recommended

- **Tesseract OCR** (for scanned PDFs)
  ```bash
  # Ubuntu/Debian
  sudo apt-get install tesseract-ocr
  
  # Mac
  brew install tesseract
  
  # Windows
  # Download from: https://github.com/UB-Mannheim/tesseract/wiki
  ```

---

## 💿 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/beginner-local-rag-cli.git
cd beginner-local-rag-cli
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv rag

# Activate virtual environment
# Linux/Mac:
source rag/bin/activate

# Windows:
rag\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install the CLI tool in editable mode
pip install -e .
```

### 4. Verify Installation

```bash
# Check if rag command is available
rag --help

# Check system status
rag manage status
```

Expected output:
```
✓ OpenSearch: Connected
✓ Ollama: Available
✓ Embedding Model: Loaded
```

---

## 🚀 Quick Start

### Step 1: Upload Your First Document

```bash
# Upload a PDF document
rag upload /path/to/your/document.pdf

# Upload with custom index name
rag upload document.pdf --index-name my_docs
```

### Step 2: Search Your Documents

```bash
# Basic search
rag search "machine learning"

# Search with more results
rag search "neural networks" --top-k 10
```

### Step 3: Chat with Your Documents

```bash
# Start interactive chat (RAG enabled)
rag chat

# Chat without RAG (direct LLM only)
rag chat --no-rag

# Chat with custom settings
rag chat --top-k 10 --temperature 0.9
```

**Chat Commands:**
- Type your question and press Enter
- Type `exit` or `quit` to end the session
- Type `clear` to clear chat history
- Press `Ctrl+C` to interrupt

---

## 📖 Commands Reference

### Upload Command

Upload and process PDF documents.

```bash
rag upload <filepath> [OPTIONS]
```

**Arguments:**
- `filepath`: Path to PDF file (required)

**Options:**
- `--index-name`: OpenSearch index name (default: `rag_index`)

**Examples:**
```bash
# Basic upload
rag upload document.pdf

# Upload to specific index
rag upload research.pdf --index-name research_docs

# Upload multiple documents
for file in *.pdf; do rag upload "$file"; done
```

**What it does:**
1. Validates PDF file
2. Copies to `uploaded_files/` directory
3. Extracts text using OCR
4. Splits into chunks (512 chars with 50 char overlap)
5. Generates embeddings (768-dimensional vectors)
6. Indexes in OpenSearch for fast retrieval

---

### Search Command

Search through indexed documents.

```bash
rag search <query> [OPTIONS]
```

**Arguments:**
- `query`: Search query (required)

**Options:**
- `--top-k`: Number of results to return (default: 5)
- `--index-name`: Index to search (default: `rag_index`)

**Examples:**
```bash
# Basic search
rag search "what is machine learning"

# Get more results
rag search "deep learning architectures" --top-k 10

# Search specific index
rag search "quantum computing" --index-name science_docs
```

**Output:**
- Ranked list of relevant text chunks
- Relevance scores
- Source document names
- Text previews

---

### Chat Command

Interactive chat with your documents.

```bash
rag chat [OPTIONS]
```

**Options:**
- `--rag / --no-rag`: Enable/disable RAG mode (default: enabled)
- `--top-k`: Number of documents to retrieve (default: 5)
- `--temperature`: LLM creativity (0.0-1.0, default: 0.7)
- `--index-name`: Index to use (default: `rag_index`)

**Examples:**
```bash
# Standard RAG chat
rag chat

# Direct LLM (no document context)
rag chat --no-rag

# More creative responses
rag chat --temperature 0.9

# Retrieve more context
rag chat --top-k 10
```

**Features:**
- Streaming responses (real-time output)
- Chat history maintained during session
- Retrieves relevant context from documents
- Commands: `exit`, `quit`, `clear`

---

### Manage Commands

System management and maintenance.

#### Check Status

```bash
rag manage status
```

Shows:
- OpenSearch connection status
- Ollama availability and models
- Embedding model status
- Number of uploaded files

#### List Indices

```bash
rag manage list-indices
```

Shows all OpenSearch indices with:
- Document count
- Index size
- Health status

#### List Documents

```bash
rag manage list-docs
```

Shows all uploaded PDF files with:
- Filename
- File size
- Last modified date

#### Delete Document

```bash
rag manage delete-doc <filename>
```

**Example:**
```bash
rag manage delete-doc research.pdf
```

Deletes all chunks associated with the document from OpenSearch.

#### Delete Index

```bash
rag manage delete-idx
```

**Warning:** This deletes the entire index and all documents!

---

## 🏗️ Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                         User (CLI)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    CLI Commands Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │  Upload  │  │  Search  │  │   Chat   │  │  Manage  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Processing Layer (src/)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   OCR    │  │Embeddings│  │Ingestion │  │   Chat   │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────┐      ┌──────────────────┐
│   OpenSearch     │      │     Ollama       │
│  (Vector Store)  │      │   (Local LLM)    │
└──────────────────┘      └──────────────────┘
```

### Data Flow: Upload

```
PDF File
   ↓
Extract Text (OCR)
   ↓
Split into Chunks (512 chars)
   ↓
Generate Embeddings (768-dim vectors)
   ↓
Store in OpenSearch
   {
     text: "chunk content",
     embedding: [0.2, 0.8, ...],
     metadata: {filename, chunk_id, ...}
   }
```

### Data Flow: Chat with RAG

```
User Query
   ↓
Generate Query Embedding
   ↓
Search OpenSearch (Hybrid: Semantic + Keyword)
   ↓
Retrieve Top-K Chunks
   ↓
Build Context from Chunks
   ↓
Prompt = System + Context + Query + History
   ↓
Send to Ollama (Streaming)
   ↓
Stream Response to User
```

---

## ⚙️ Configuration

### Configuration File

The system uses constants defined in `src/constants.py`:

```python
# Embedding Model
EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
EMBEDDING_DIMENSION = 768

# Text Processing
TEXT_CHUNK_SIZE = 300
CHUNK_SIZE = 512
CHUNK_OVERLAP = 50

# LLM
OLLAMA_MODEL_NAME = "llama3.2:1b"

# OpenSearch
OPENSEARCH_HOST = "localhost"
OPENSEARCH_PORT = 9200
OPENSEARCH_INDEX = "documents"

# Logging
LOG_FILE_PATH = "logs/app.log"
```

### Customization

To customize settings, edit `src/constants.py`:

**Change LLM Model:**
```python
OLLAMA_MODEL_NAME = "llama2"  # or "mistral", "codellama", etc.
```

**Change Embedding Model:**
```python
EMBEDDING_MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"  # Faster, smaller
EMBEDDING_DIMENSION = 384  # Must match model output dimension
```

**Adjust Chunking:**
```python
CHUNK_SIZE = 1024  # Larger chunks = more context, fewer chunks
CHUNK_OVERLAP = 100  # More overlap = better continuity
```

**OpenSearch Settings:**
```python
OPENSEARCH_HOST = "192.168.1.100"  # Remote OpenSearch instance
OPENSEARCH_PORT = 9200
```

---

## 🐛 Troubleshooting

### OpenSearch Connection Failed

**Error:**
```
✗ OpenSearch: Disconnected
Error: ConnectionError
```

**Solutions:**
1. Check if OpenSearch is running:
   ```bash
   curl -X GET "localhost:9200"
   ```

2. Restart OpenSearch (Docker):
   ```bash
   docker restart opensearch-node
   ```

3. Check firewall settings (port 9200 should be open)

---

### Ollama Model Not Found

**Error:**
```
✗ Ollama: Unavailable
Error: Model 'llama3.2:1b' not found
```

**Solutions:**
1. Pull the model:
   ```bash
   ollama pull llama3.2:1b
   ```

2. Check available models:
   ```bash
   ollama list
   ```

3. Verify Ollama is running:
   ```bash
   curl http://localhost:11434/api/tags
   ```

---

### Embedding Model Download Issues

**Error:**
```
✗ Embedding Model: Failed
Error: Failed to download model
```

**Solutions:**
1. Check internet connection
2. Manually download model:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
   ```

3. Use a local model path in `src/constants.py`:
   ```python
   EMBEDDING_MODEL_PATH = "path/to/local/model"
   ```

---

### Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'click'
```

**Solutions:**
1. Ensure virtual environment is activated:
   ```bash
   source rag/bin/activate  # Linux/Mac
   rag\Scripts\activate     # Windows
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Reinstall CLI:
   ```bash
   pip install -e .
   ```

---

### PDF Processing Errors

**Error:**
```
Error: Failed to extract text from PDF
```

**Solutions:**
1. Install Tesseract OCR (for scanned PDFs)
2. Check PDF is not corrupted:
   ```bash
   file document.pdf
   ```
3. Try a different PDF to isolate the issue

---

### Memory Issues

**Error:**
```
Error: CUDA out of memory / RAM error
```

**Solutions:**
1. Use a smaller model:
   ```python
   OLLAMA_MODEL_NAME = "llama3.2:1b"  # Smallest option
   ```

2. Use CPU instead of GPU:
   ```python
   # In src/embeddings.py
   device = "cpu"
   ```

3. Reduce chunk size:
   ```python
   CHUNK_SIZE = 256
   ```

---

## 📁 Project Structure

```
beginner-local-rag-cli/
├── cli/                          # CLI application code
│   ├── __init__.py
│   ├── main.py                   # Entry point
│   └── commands/                 # Command implementations
│       ├── __init__.py
│       ├── upload.py             # Upload command
│       ├── chat.py               # Chat command
│       ├── search.py             # Search command
│       └── manage.py             # Management commands
│
├── src/                          # Core RAG functionality
│   ├── __init__.py
│   ├── chat.py                   # LLM chat logic
│   ├── embeddings.py             # Embedding generation
│   ├── opensearch.py             # Search functionality
│   ├── ingestion.py              # Document processing
│   ├── ocr.py                    # PDF text extraction
│   ├── constants.py              # Configuration
│   ├── utils.py                  # Utilities
│   └── index_config.json         # OpenSearch schema
│
├── data/
│   └── uploaded_files/           # Uploaded PDFs stored here
│
├── logs/
│   └── app.log                   # Application logs
│
├── setup.py                      # Package installation config
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── .gitignore                    # Git ignore rules
```

---

## 🔑 Key Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| **Click** | CLI framework | 8.0+ |
| **Rich** | Beautiful terminal output | 13.0+ |
| **OpenSearch** | Vector database | 2.x |
| **Ollama** | Local LLM runtime | Latest |
| **SentenceTransformers** | Text embeddings | Latest |
| **LangChain** | Text processing utilities | Latest |
| **PyPDF2/pdf2image** | PDF processing | Latest |

---

## 📊 Performance Tips

### For Faster Uploads

1. **Use smaller embedding models:**
   ```python
   EMBEDDING_MODEL_PATH = "sentence-transformers/all-MiniLM-L6-v2"
   ```

2. **Increase chunk size:**
   ```python
   CHUNK_SIZE = 1024  # Fewer chunks to process
   ```

3. **Use GPU if available:**
   ```python
   device = "cuda"  # In src/embeddings.py
   ```

### For Better Search Quality

1. **Use larger embedding models:**
   ```python
   EMBEDDING_MODEL_PATH = "sentence-transformers/all-mpnet-base-v2"
   ```

2. **Increase top-k:**
   ```bash
   rag search "query" --top-k 10
   ```

3. **Optimize chunk size:**
   ```python
   CHUNK_SIZE = 512
   CHUNK_OVERLAP = 100  # More context preservation
   ```

### For Better Chat Responses

1. **Use larger LLM:**
   ```bash
   ollama pull llama2  # or llama3
   ```

2. **Increase retrieval:**
   ```bash
   rag chat --top-k 10
   ```

3. **Adjust temperature:**
   ```bash
   rag chat --temperature 0.3  # More focused
   rag chat --temperature 0.9  # More creative
   ```

---

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit with descriptive message:**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to your fork:**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/beginner-local-rag-cli.git
cd beginner-local-rag-cli

# Create virtual environment
python -m venv rag
source rag/bin/activate

# Install in development mode
pip install -e ".[dev]"

# Run tests (if available)
pytest
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Original Streamlit project: [jamwithai/beginner-local-rag-system](https://github.com/jamwithai/beginner-local-rag-system)
- OpenSearch for vector search capabilities
- Ollama for local LLM inference
- Hugging Face for pre-trained models

---

## 📧 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/beginner-local-rag-cli/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/beginner-local-rag-cli/discussions)

---

## 🗺️ Roadmap

- [ ] Support for more document types (DOCX, TXT, HTML)
- [ ] Web interface option
- [ ] Docker compose for easy setup
- [ ] Batch upload command
- [ ] Export/import index functionality
- [ ] Advanced query operators
- [ ] Multiple index management
- [ ] API server mode

---

## 📈 Changelog

### Version 1.0.0 (Current)
- Initial CLI release
- PDF upload and processing
- Hybrid search (semantic + keyword)
- Interactive chat with RAG
- System management commands
- Rich terminal UI

---

**Made with ❤️ for privacy-conscious AI enthusiasts**

*Remember: Your data stays on your machine. Always.*