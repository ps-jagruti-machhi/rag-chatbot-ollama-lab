<h1>Build a local RAG with Ollama</h1>

<h2>Watch the full tutorial on my YouTube Channel</h2>
<div>

<a href="https://youtu.be/c5jHhMXmXyo">
    <img src="thumbnail_small.png" alt="Thomas Janssen Youtube" width="200"/>
</a>
</div>

<h2>Prerequisites</h2>
<ul>
  <li>Python 3.11+</li>
</ul>

<h2>Installation</h2>
<h3>1. Clone the repository:</h3>

```
git clone https://github.com/ThomasJanssen-tech/Local-RAG-with-Ollama
cd Local-RAG-With-Ollama
```

<h3>2. Create a virtual environment</h3>

```
python -m venv venv
```

<h3>3. Activate the virtual environment</h3>

```
venv\Scripts\Activate
(or on Mac): source venv/bin/activate
```

<h3>4. Install libraries</h3>

```
pip install -r requirements.txt
```

<h3>5. Add Bright Data API Key</h3>
<ul>
<li>Get your $15 Bright Data credits: https://brdta.com/tomstechacademy</li>
<li>Rename the .env.example file to .env</li>
<li>Add your Bright Data API key</li>
<li><i>If you want to use ChatGPT or Anthropic models, add an API key (not required for Ollama)</i></li>
</ul>

<h2>Executing the scripts</h2>

<h3>Step-by-Step Execution Guide</h3>

<p>This application consists of three main scripts that must be executed in sequence:</p>

<h4>Step 1: Data Scraping</h4>
<p>Scrapes Wikipedia articles based on keywords defined in <code>keywords.xlsx</code>.</p>

```bash
python 1_scraping_wikipedia.py
```

<p><strong>Output:</strong> Creates a <code>datasets/</code> folder containing scraped Wikipedia articles in JSON format.</p>

<h4>Step 2: Chunking, Embedding & Ingestion</h4>
<p>Processes the scraped data by chunking text, creating embeddings, and storing them in ChromaDB.</p>

```bash
python 2_chunking_embedding_ingestion.py
```

or

```
cd Local-RAG-with-Ollama
python -m streamlit run 3_chatbot.py
```

<p><strong>Output:</strong> Creates a <code>chroma_db/</code> folder containing the vector database with embedded chunks.</p>

<h4>Step 3: Launch the Chatbot</h4>
<p>Starts the Streamlit-based RAG chatbot interface.</p>

```bash
streamlit run 3_chatbot.py
```

<p><strong>Output:</strong> Opens a web browser at <code>http://localhost:8501</code> with the chatbot interface.</p>

<h3>Quick Start (Windows)</h3>
<p>For Windows users, you can use the provided batch file to run all steps:</p>

```bash
run.bat
```

<p>This will execute all three scripts in sequence automatically.</p>

<h3>Quick Start (From Parent Directory)</h3>
<p>If you're in the parent directory, use the provided batch file:</p>

```bash
run-chatbot.bat
```

<p>This command navigates to the <code>Local-RAG-with-Ollama</code> directory and runs:</p>

```bash
python -m streamlit run 3_chatbot.py
```

<h3>Important Notes</h3>
<ul>
  <li><strong>Prerequisites:</strong> Ensure Ollama is installed and running on your system. Download from <a href="https://ollama.com">https://ollama.com</a></li>
  <li><strong>Model Requirements:</strong> The application uses <code>mxbai-embed-large</code> for embeddings and <code>qwen3</code> for chat. Pull these models in Ollama:
    <ul>
      <li><code>ollama pull mxbai-embed-large</code></li>
      <li><code>ollama pull qwen3</code></li>
    </ul>
  </li>
  <li><strong>First Run:</strong> Always run Steps 1 and 2 before launching the chatbot to ensure data is available.</li>
  <li><strong>Re-running:</strong> If you modify the keywords in <code>keywords.xlsx</code>, re-run Steps 1 and 2 to update the knowledge base.</li>
  <li><strong>Environment Variables:</strong> Ensure your <code>.env</code> file is properly configured with the Bright Data API key.</li>
</ul>

<h3>Troubleshooting</h3>
<ul>
  <li><strong>Import Errors:</strong> Make sure the virtual environment is activated and all dependencies are installed.</li>
  <li><strong>Ollama Connection:</strong> Verify Ollama is running by checking <code>http://localhost:11434</code> in your browser.</li>
  <li><strong>Empty Results:</strong> Check that <code>keywords.xlsx</code> contains valid Wikipedia search terms.</li>
  <li><strong>Port Conflicts:</strong> If port 8501 is in use, Streamlit will automatically try the next available port.</li>
</ul>

<h2>Further reading</h2>
<ul>
<li>https://www.ibm.com/think/topics/vector-embedding</li>
<li>https://ollama.com/blog/embedding-models</li>
<li>https://python.langchain.com/docs/integrations/vectorstores/chroma/</li>
<li>https://python.langchain.com/docs/integrations/text_embedding/ollama/</li>
<li>https://ollama.com/library/mxbai-embed-large</li>
<li>https://ollama.com/library/qwen3</li>
</ul>
