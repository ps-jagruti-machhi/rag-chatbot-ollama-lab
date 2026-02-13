#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import json
import pandas as pd
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from uuid import uuid4
import shutil
import time
import re
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

load_dotenv()

###############################   INITIALIZE EMBEDDINGS MODEL  #################################################################################################

embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

###############################   INITIALIZE CHROMA VECTOR STORE   ############################################################################################

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"),
)

###############################   INITIALIZE TEXT SPLITTER   ###################################################################################################

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

#################################################################################################################################################################
###############################   2.  PROCESSING THE DATA FILE   ###############################################################################################
#################################################################################################################################################################

def parse_custom_format(file_path):
    """Parse the custom text format from the alternative scraping script."""
    articles = []
    
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    
    # Split by the separator
    sections = content.split("=" * 80)
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        # Extract title
        title_match = re.search(r'===\s*(.+?)\s*===', section)
        if not title_match:
            continue
        
        title = title_match.group(1)
        
        # Extract keyword
        keyword_match = re.search(r'Keyword:\s*(.+)', section)
        keyword = keyword_match.group(1).strip() if keyword_match else ""
        
        # Extract URL
        url_match = re.search(r'URL:\s*(.+)', section)
        url = url_match.group(1).strip() if url_match else ""
        
        # Extract content (everything after URL until the end)
        content_start = section.find("URL:")
        if content_start != -1:
            # Find the end of the URL line
            url_end = section.find("\n", content_start)
            if url_end != -1:
                raw_text = section[url_end + 1:].strip()
            else:
                raw_text = ""
        else:
            raw_text = ""
        
        if raw_text:
            articles.append({
                "url": url,
                "raw_text": raw_text,
                "title": title
            })
    
    return articles

def parse_json_format(file_path):
    """Parse JSON lines format from the original scraping script."""
    articles = []
    
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            articles.append(obj)
    
    return articles

# Try to parse the data file
data_file = os.getenv("DATASET_STORAGE_FOLDER") + "data.txt"

try:
    # First try custom format (since that's what the alternative scraper produces)
    file_content = parse_custom_format(data_file)
    print(f"Parsed {len(file_content)} articles from custom format")
except Exception as e:
    try:
        # Fall back to JSON format
        file_content = parse_json_format(data_file)
        print(f"Parsed {len(file_content)} articles from JSON format")
    except Exception as e2:
        print(f"Error parsing data file: {e}")
        file_content = []

#################################################################################################################################################################
###############################   3.  CHUNKING, EMBEDDING AND INGESTION   #######################################################################################
##################################################################################################################################################################

if file_content:
    for line in file_content:
        
        print(f"Processing: {line.get('title', 'Unknown')}")
        print(f"URL: {line.get('url', 'Unknown')}")
        
        texts = []
        texts = text_splitter.create_documents(
            [line['raw_text']], 
            metadatas=[{"source": line['url'], "title": line['title']}]
        )
        
        uuids = [str(uuid4()) for _ in range(len(texts))]
        
        vector_store.add_documents(documents=texts, ids=uuids)
        print(f"Added {len(texts)} chunks to vector store")
        print()
    
    print(f"\nSuccessfully ingested {len(file_content)} articles into the vector store")
else:
    print("No articles found to ingest. Please run the scraping script first.")