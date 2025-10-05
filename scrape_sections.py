import requests
from bs4 import BeautifulSoup
import json
import time
import os

# Define base url for IPC at bareactslive
BASE_URL = "" # TODO: add the base url of the website to be crawled

# Placeholder list for all sections
ipc_sections = []
json_file = "ipc_sections.json"

# Load existing data if file exists
if os.path.exists(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        try:
            ipc_sections = json.load(f)
        except json.JSONDecodeError:
            ipc_sections = []

# List of missing/extra sections to scrape (updated from user)
missing_sections = [
    "29A"
]

for section_num in list(range(1, 512)) + missing_sections:
    url = f"{BASE_URL}{section_num}/"  # Adjust URL pattern per site
    print(f"Fetching Section {section_num} from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract mys-head and mys-desc
        heads = []
        for el in soup.find_all(class_="mys-head"):
            # Remove all elements with class 'nowrap' inside this mys-head
            for nowrap in el.find_all(class_="nowrap"):
                nowrap.decompose()
            heads.append(el.get_text(separator="\n", strip=True))
        descs = [el.get_text(separator="\n", strip=True) for el in soup.find_all(class_="mys-desc")]
        text_content = "\n".join(heads + descs)

        if isinstance(heads, list):
            heads = "\n".join(heads)
        if isinstance(descs, list):
            descs = "\n".join(descs)

        ipc_sections.append({
            "document_id": "ipc-1860",
            "section_number": str(section_num),
            "section_title": f"Section {section_num}: {heads}",
            "section_text": f"{descs}",
            "citation": f"IPC Section {section_num}",
            "document_title": "Indian Penal Code, 1860",
            "jurisdiction": "India",
            "date": "1860-10-06"
        })

        time.sleep(0.2)  # Be polite to server

    except Exception as e:
        print(f"Error fetching section {section_num}: {e}")

# Write all data back to file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(ipc_sections, f, ensure_ascii=False, indent=2)

print("Extraction completed. Data saved to ipc_sections.json")
