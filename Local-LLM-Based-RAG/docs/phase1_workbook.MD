# 📖 Phase 1 Workbook: Understanding the Original RAG System

## 🎯 Objective
By the end of this phase, you'll have a complete mental model of how the original Streamlit RAG system works.

---

## 📋 Exercise 1: Code Structure Analysis

### Task 1.1: Create Your Own Documentation

Open each file and answer these questions:

#### File: `Welcome.py`
**Location**: Root directory
**Purpose**: Main entry point for Streamlit app

**Questions to Answer:**
1. What does this file do when you run `streamlit run Welcome.py`?
   
   **Your Answer:**
   ________________________________________________
   ________________________________________________

2. What Streamlit components does it use?
   - [ ] st.title()
   - [ ] st.write()
   - [ ] st.button()
   - [ ] Other: ______________

3. Does it import anything from `src/`? List them:
   
   **Your Answer:**
   ________________________________________________

---

#### File: `src/constants.py`
**Purpose**: Configuration constants

**Your Analysis:**
```python
# Copy the actual values you find:

OPENSEARCH_HOST = "_______________"
OPENSEARCH_PORT = _______________
INDEX_NAME = "_______________"
EMBEDDING_MODEL_PATH = "_______________"

# Add any other constants you find:
# _______________
# _______________
```

**Questions:**
1. Why are these values hardcoded instead of in environment variables?
2. What would you improve?

---

#### File: `src/embeddings.py`
**Purpose**: Generate vector embeddings

**Code Reading Exercise:**
```python
# Find the main function and write its signature:

def _______________(_______________, _______________):
    """
    What does this function do?
    ________________________________
    """
    pass
```

**Questions:**
1. What model is used for embeddings?
   - Answer: _______________

2. What is the output format?
   - [ ] List of numbers
   - [ ] Numpy array
   - [ ] Tensor
   - [ ] Other: ______________

3. How long are the embedding vectors?
   - Answer: _______________ dimensions

---

#### File: `src/opensearch_utils.py`
**Purpose**: OpenSearch operations

**Functions Inventory:**
List all functions you find:
```
1. _______________() - Does: _______________
2. _______________() - Does: _______________
3. _______________() - Does: _______________
4. _______________() - Does: _______________
```

**Deep Dive:**
Pick one function and explain what it does:
```python
# Function name: _______________

# What it takes as input:
# _______________

# What it returns:
# _______________

# How it works (in your own words):
# _______________
# _______________
```

---

#### File: `src/ocr.py`
**Purpose**: Extract text from PDFs

**Questions:**
1. What library is used for OCR?
   - Answer: _______________

2. When is OCR used vs direct text extraction?
   
   **Your Answer:**
   ________________________________________________

3. What image formats are supported?
   - [ ] PNG
   - [ ] JPEG
   - [ ] Other: ______________

---

#### File: `pages/chat.py`
**Purpose**: Chat interface

**Flow Diagram Exercise:**
Draw the user flow:
```
User opens chat page
     ↓
[What happens? Fill in the steps]
     ↓
     ?
     ↓
     ?
     ↓
Result displayed
```

**Streamlit Session State:**
List all session state variables used:
```
st.session_state._______________
st.session_state._______________
st.session_state._______________
```

---

## 📋 Exercise 2: Data Flow Analysis

### Task 2.1: Trace Document Upload

**Starting Point**: User uploads a PDF in Streamlit

**Your Mission**: Follow the code and fill in each step:

```
1. PDF uploaded via st.file_uploader()
   ↓
   File: _______________
   Function: _______________

2. PDF is processed
   ↓
   File: _______________
   Function: _______________
   Output: _______________

3. Text is chunked
   ↓
   File: _______________
   Function: _______________
   Chunk size: _______________

4. Embeddings generated
   ↓
   File: _______________
   Function: _______________
   Model used: _______________

5. Stored in OpenSearch
   ↓
   File: _______________
   Function: _______________
   Index name: _______________
```

### Task 2.2: Trace Search Query

**Starting Point**: User enters search query

```
1. Query entered: "_______________"
   ↓
   Function called: _______________

2. Query is embedded
   ↓
   Same embedding model? Yes / No
   Output dimensions: _______________

3. Search performed
   ↓
   Search type: [ ] Keyword [ ] Semantic [ ] Hybrid
   Top K results: _______________

4. Results displayed
   ↓
   What information is shown?
   - _______________
   - _______________
```

---

## 📋 Exercise 3: Dependency Analysis

### Task 3.1: List All Dependencies

Open `requirements.txt` and categorize:

**UI/Framework:**
- streamlit
- _______________

**ML/Embeddings:**
- sentence-transformers
- _______________

**Search:**
- opensearch-py
- _______________

**Document Processing:**
- PyPDF2
- _______________

**Other:**
- _______________

### Task 3.2: Which Can Be Removed for CLI?

**Mark for removal:**
- [ ] streamlit (definitely!)
- [ ] sentence-transformers (keep)
- [ ] opensearch-py (keep)
- [ ] Other: ______________

**Need to add for CLI:**
- [ ] click
- [ ] rich
- [ ] Other: ______________

---

## 📋 Exercise 4: Pain Points & Improvements

### Task 4.1: Current Limitations

**What doesn't work well in Streamlit version?**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Task 4.2: CLI Advantages

**How will CLI be better?**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## 📋 Exercise 5: Architecture Diagram

### Task 5.1: Draw the System

Create a diagram showing:
```
[User] → [Streamlit UI] → [???] → [OpenSearch]
                    ↓
              [Embedding Model]
                    ↓
                  [LLM?]
```

**Fill in the missing pieces!**

---

## 📋 Exercise 6: Configuration Discovery

### Task 6.1: Find All Configurable Values

**Search the code for:**
- Hardcoded paths
- URLs
- Port numbers
- Model names
- Timeouts
- etc.

**Create a list:**
```
1. OpenSearch host: _______________
2. OpenSearch port: _______________
3. Embedding model: _______________
4. Chunk size: _______________
5. _______________
```

### Task 6.2: Design Your Config

**How would YOU configure these in a CLI app?**
- [ ] .env file
- [ ] YAML config
- [ ] Command-line flags
- [ ] All of the above!

---

## 📋 Exercise 7: Testing the Original App

### Task 7.1: Run the App

```bash
cd local-rag-system
streamlit run Welcome.py
```

**Document your experience:**
1. Did it start successfully? Yes / No
2. Any errors? _______________
3. What do you see on the welcome page?
   ________________________________________________

### Task 7.2: Upload a Document

1. Create a test PDF with some text
2. Upload it through the UI
3. **Document what happens:**
   - Processing time: _______________
   - Any errors? _______________
   - Can you see the chunks? Yes / No

### Task 7.3: Try a Search

1. Enter a query: "_______________"
2. **Results:**
   - Number of results: _______________
   - Relevant? Yes / No
   - Response time: _______________

---

## 📋 Exercise 8: Code Quality Review

### Task 8.1: Find Areas for Improvement

**Look for:**
- [ ] Hardcoded values
- [ ] Missing error handling
- [ ] No logging
- [ ] Unclear variable names
- [ ] Mixed concerns (UI + logic)

**Document 3 specific improvements:**
1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## ✅ Phase 1 Completion Checklist

Before moving to Phase 2, ensure you can answer:

- [ ] What is the purpose of each file in `src/`?
- [ ] How does document processing work?
- [ ] How does search work?
- [ ] What is the role of embeddings?
- [ ] What are the main dependencies?
- [ ] What needs to change for CLI?
- [ ] Where is the business logic vs UI?

---

## 🎓 Knowledge Check

### Quiz Yourself:

1. **What library generates embeddings?**
   Answer: _______________

2. **What vector database is used?**
   Answer: _______________

3. **Can you run multiple searches without reloading?**
   Answer: _______________

4. **Where is the chat history stored?**
   Answer: _______________

5. **What happens if OpenSearch is not running?**
   Answer: _______________

---

## 📝 Reflection

**What surprised you most about the codebase?**
_______________________________________________
_______________________________________________

**What's the most complex part?**
_______________________________________________
_______________________________________________

**What are you most excited to improve in CLI version?**
_______________________________________________
_______________________________________________

---

## 🚀 Ready for Phase 2?

Once you've completed this workbook, you're ready to start building the CLI!

**Next**: [Phase 2 - CLI Foundation](./PHASE_2_WORKBOOK.md)

---

**Pro Tip**: Keep this workbook! You'll reference it often when building the CLI version.