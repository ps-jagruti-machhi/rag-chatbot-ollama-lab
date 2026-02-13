#################################################################################################################################################################
###############################   1.  IMPORTING MODULES AND INITIALIZING VARIABLES   ############################################################################
#################################################################################################################################################################

from dotenv import load_dotenv
import os
import requests
import json
import pandas as pd
import glob
import certifi
import urllib3

# Suppress SSL warnings for development/testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

pd.options.mode.chained_assignment = None

load_dotenv()

###############################   HEADERS (DON'T CHANGE)   #######################################################################################################
headers = {
    'Authorization': 'Bearer '+os.getenv('BRIGHTDATA_API_KEY'),
    'Content-Type': 'application/json',
}

headers_status = {
    'Authorization': 'Bearer '+os.getenv('BRIGHTDATA_API_KEY'),
}

keywords = pd.read_excel("keywords.xlsx")

def _requests_verify_kwargs():
    ca_bundle = os.getenv("REQUESTS_CA_BUNDLE") or os.getenv("BRIGHTDATA_CA_BUNDLE")
    if ca_bundle:
        return {"verify": ca_bundle}
    # Disable SSL verification for development/testing
    return {"verify": False}

#################################################################################################################################################################
###############################   2.  IF SnapshotID IS NOT SET IN .XLSX FILE, TRIGGER CREATION OF THE SNAPSHOT   ################################################
#################################################################################################################################################################

file_exists = os.path.isfile(os.getenv("SNAPSHOT_STORAGE_FILE"))


if not file_exists:

    params = {
        "dataset_id": "gd_lr9978962kkjr3nx49",
        "include_errors": "true",
        "type": "discover_new",
        "discover_by": "keyword",
    }

    json_data = []

    for ind in keywords.index:

        json_data.append({"keyword":keywords.loc[ind, "Keyword"],"pages_load":str(keywords.loc[ind, "Pages"])})

    response = requests.post(
        'https://api.brightdata.com/datasets/v3/trigger',
        params=params,
        headers=headers,
        json=json_data,
        **_requests_verify_kwargs()
    )

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.content.decode('utf-8')}")
    
    # Check if response is valid JSON
    try:
        result = json.loads(response.content)
        
        with open(os.getenv("SNAPSHOT_STORAGE_FILE"), "a") as f:
            f.write(str(result["snapshot_id"]))
            
        print(f"Snapshot created successfully with ID: {result['snapshot_id']}")
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse JSON response from BrightData API")
        print(f"Response content: {response.content.decode('utf-8')}")
        print(f"This usually means your BrightData API key is invalid or the account is not active.")
        print(f"Please check your BRIGHTDATA_API_KEY in the .env file.")
        exit(1)


else:

#################################################################################################################################################################
###############################   3.  IF SnapshotID IS SET, GET BACK THE CRAWLED DATA   #########################################################################
#################################################################################################################################################################


###############################   CHECK WHETHER ALL WEBSITES ARE CRAWLED   #######################################################################################

    files = glob.glob(os.getenv("DATASET_STORAGE_FOLDER")+"*")	

    for f in files:
        os.remove(f)



    f = open(os.getenv("SNAPSHOT_STORAGE_FILE"),"r")
    snapshot_id = f.read()

    response = requests.get(
        'https://api.brightdata.com/datasets/v3/progress/' + snapshot_id,
        headers=headers_status,
        **_requests_verify_kwargs()
    )
    
    status = response.json()['status']

    print("status")
    print(status)


    snapshot_ready = False

    if(status == "ready"):
        print("Snapshot is ready")
        snapshot_ready = True
    else:
        print("Snapshot is NOT READY YET")


    print("")

###############################   IF ALL WEBSITES ARE READY, FETCH DATA AND WRITE TO FILES   ######################################################################

    if snapshot_ready:
        print("== > All articles are ready - start writing data to datasets directory")


        response = requests.get(
            'https://api.brightdata.com/datasets/v3/snapshot/' + snapshot_id,
            headers=headers,
            **_requests_verify_kwargs()
        )

        if not os.path.exists(os.getenv("DATASET_STORAGE_FOLDER")):
             os.makedirs(os.getenv("DATASET_STORAGE_FOLDER"))

        with open(os.getenv("DATASET_STORAGE_FOLDER")+"data.txt", "wb") as f:
            f.write(response.content)

    else:
         print("== > Not all articles are scraped yet - try again in a few minutes")
