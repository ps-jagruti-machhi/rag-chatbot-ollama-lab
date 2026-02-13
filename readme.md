# RAG Chatbot with Ollama

Build a local RAG (Retrieval-Augmented Generation) pipeline using Ollama for embeddings and chat, with Wikipedia scraping, ChromaDB vector storage, and a Streamlit UI.

## Prerequisites

- Python 3.11+
- Ollama installed and running ([Download Ollama](https://ollama.com))

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/ps-jagruti-machhi/rag-chatbot-ollama-lab
cd rag-chatbot-ollama-lab
```

### 2. Create a virtual environment:

```bash
python -m venv venv
```

### 3. Activate the virtual environment:

**Windows:**
```bash
venv\Scripts\Activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install required libraries:

```bash
pip install -r requirements.txt
```

### 5. Pull Ollama models:

```bash
ollama pull mxbai-embed-large
ollama pull llama3.2:3b
```

### 6. Create a `.env` file:

Create a `.env` file in the project root with the following configuration:

```env
# == OLLAMA == #
EMBEDDING_MODEL = "mxbai-embed-large"
CHAT_MODEL = "llama3.2:3b"
MODEL_PROVIDER = "ollama"

# == BRIGHTDATA (Optional - for original scraping script) == #
BRIGHTDATA_API_KEY = "your-api-key-here"

# == ENV VARS == #
DATASET_STORAGE_FOLDER = "datasets/"
SNAPSHOT_STORAGE_FILE = "snapshot.txt"

# == CHROMA COLLECTION NAME == #
DATABASE_LOCATION = "chroma_db"
COLLECTION_NAME = "rag_data"
```

**Note:** The `.env` file is not included in the repository for security reasons. You need to create it yourself.

## Executing the Scripts

### Option 1: Using the alternative Wikipedia scraping (No API key required)

```bash
python 1_scraping_wikipedia_alternative.py
python 2_chunking_embedding_ingestion.py
python -m streamlit run 3_chatbot.py
```

### Option 2: Using Bright Data scraping (Requires API key)

```bash
python 1_scraping_wikipedia.py
python 2_chunking_embedding_ingestion.py
python -m streamlit run 3_chatbot.py
```

### Option 3: Using batch file (Windows)

```bash
run.bat
```

## Project Structure

```
rag-chatbot-ollama-lab/
├── 1_scraping_wikipedia.py              # Original Wikipedia scraping (Bright Data)
├── 1_scraping_wikipedia_alternative.py  # Alternative Wikipedia scraping (Free API)
├── 2_chunking_embedding_ingestion.py    # Chunking and embedding to ChromaDB
├── 3_chatbot.py                         # Streamlit chatbot UI
├── keywords.xlsx                       # Keywords to search for
├── requirements.txt                     # Python dependencies
├── .gitignore                           # Git ignore rules
├── .streamlit/
│   └── config.toml                     # Streamlit configuration
├── datasets/                           # Scraped data storage
└── chroma_db/                           # Vector database storage
```

## Configuration

### Using Different Models

**Ollama (Default):**
```env
EMBEDDING_MODEL = "mxbai-embed-large"
CHAT_MODEL = "llama3.2:3b"
MODEL_PROVIDER = "ollama"
```

**OpenAI:**
```env
CHAT_MODEL = "gpt-4o-mini"
MODEL_PROVIDER = "openai"
OPENAI_API_KEY = "sk-your-key"
```

**Anthropic:**
```env
CHAT_MODEL = "claude-3-7-sonnet-20250219"
MODEL_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = "anthropic-your-key"
```

## How It Works

1. **Scraping:** Fetches Wikipedia articles based on keywords from `keywords.xlsx`
2. **Chunking:** Splits articles into smaller text chunks
3. **Embedding:** Converts text chunks into vector embeddings using Ollama
4. **Storage:** Stores embeddings in ChromaDB vector database
5. **Retrieval:** When a user asks a question, retrieves relevant chunks
6. **Generation:** Uses the LLM to generate answers based on retrieved context

## Troubleshooting

### ModuleNotFoundError: No module named 'streamlit'

Make sure you've installed the requirements:
```bash
pip install -r requirements.txt
```

### Connection error to Ollama

Ensure Ollama is running:
```bash
ollama serve
```

### Bright Data API not working

Use the alternative scraping script that doesn't require an API key:
```bash
python 1_scraping_wikipedia_alternative.py
```

## Further Reading

- [Vector Embeddings - IBM](https://www.ibm.com/think/topics/vector-embedding)
- [Ollama Embedding Models](https://ollama.com/blog/embedding-models)
- [LangChain Chroma Integration](https://python.langchain.com/docs/integrations/vectorstores/chroma/)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/text_embedding/ollama/)
- [mxbai-embed-large Model](https://ollama.com/library/mxbai-embed-large)
- [llama3.2 Model](https://ollama.com/library/llama3.2)

## License

This project is for educational purposes.
