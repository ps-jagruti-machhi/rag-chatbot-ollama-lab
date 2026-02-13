#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
import glob
import urllib3

# Suppress SSL warnings for development/testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

# Wikipedia API endpoint
WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

# Wikipedia requires a User-Agent header
WIKIPEDIA_HEADERS = {
    "User-Agent": "LocalRAGBot/1.0 (https://github.com; educational_purpose@example.com)"
}

keywords = pd.read_excel("keywords.xlsx")

#################################################################################################################################################################
###############################   2.  SCRAPE WIKIPEDIA USING FREE WIKIPEDIA API   ##############################################################################
#################################################################################################################################################################

def scrape_wikipedia(keyword, pages=1):
    """
    Scrape Wikipedia articles using the free Wikipedia MediaWiki API
    """
    print(f"Scraping Wikipedia for keyword: {keyword}")
    
    # Search for articles matching the keyword
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": keyword,
        "format": "json",
        "srlimit": pages * 5  # Get more results to filter
    }
    search_response = requests.get(WIKIPEDIA_API_URL, params=search_params, headers=WIKIPEDIA_HEADERS, verify=False)
    
    print(f"Status Code: {search_response.status_code}")
    print(f"Response: {search_response.text[:500]}")
    
    if search_response.status_code != 200:
        print(f"Error: Wikipedia API returned status {search_response.status_code}")
        return []
    
    search_data = search_response.json()
    
    articles = []
    
    if "query" in search_data and "search" in search_data["query"]:
        for result in search_data["query"]["search"][:pages]:
            title = result["title"]
            
            # Get full article content
            content_params = {
                "action": "query",
                "prop": "extracts",
                "explaintext": True,
                "exintro": False,
                "titles": title,
                "format": "json"
            }
            
            content_response = requests.get(WIKIPEDIA_API_URL, params=content_params, headers=WIKIPEDIA_HEADERS, verify=False)
            content_data = content_response.json()
            
            # Extract the page content
            pages_data = content_data["query"]["pages"]
            for page_id, page_data in pages_data.items():
                if "extract" in page_data:
                    articles.append({
                        "keyword": keyword,
                        "title": page_data["title"],
                        "content": page_data["extract"],
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    })
    
    return articles

#################################################################################################################################################################
###############################   3.  MAIN EXECUTION   ###########################################################################################
#################################################################################################################################################################

# Clear existing datasets
dataset_folder = os.getenv("DATASET_STORAGE_FOLDER", "datasets/")
if os.path.exists(dataset_folder):
    files = glob.glob(dataset_folder + "*")
    for f in files:
        if os.path.isfile(f):
            os.remove(f)

# Create datasets folder if it doesn't exist
if not os.path.exists(dataset_folder):
    os.makedirs(dataset_folder)

# Scrape all keywords
all_articles = []

for ind in keywords.index:
    keyword = keywords.loc[ind, "Keyword"]
    pages = keywords.loc[ind, "Pages"]
    
    articles = scrape_wikipedia(keyword, pages)
    all_articles.extend(articles)
    print(f"Found {len(articles)} articles for '{keyword}'")

# Save all articles to a JSON file
output_file = os.path.join(dataset_folder, "data.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

# Also save as text file for compatibility with the original script
text_file = os.path.join(dataset_folder, "data.txt")
with open(text_file, "w", encoding="utf-8") as f:
    for article in all_articles:
        f.write(f"=== {article['title']} ===\n")
        f.write(f"Keyword: {article['keyword']}\n")
        f.write(f"URL: {article['url']}\n")
        f.write(f"\n{article['content']}\n")
        f.write("\n" + "="*80 + "\n\n")

print(f"\n✅ Successfully scraped {len(all_articles)} articles")
print(f"📁 Data saved to: {output_file}")
print(f"📁 Data saved to: {text_file}")