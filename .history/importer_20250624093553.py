import os
import csv
import json
import re
import html.parser
import mimetypes
import requests
import sys
import locale
import time

# Set the default encoding to the system's preferred encoding
sys.stdin.reconfigure(encoding=locale.getpreferredencoding())
sys.stdout.reconfigure(encoding=locale.getpreferredencoding())

def validate_url(url):
    """Checks whether a URL is valid and accessible."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def parse_markdown(filepath):
    """Parses a Markdown file and extracts links."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        content = f.read()
    # Match Markdown links in format [title](url)
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
    return [{'url': url, 'title': title} for title, url in links]

def parse_file(filepath):
    """Recognizes file type and extracts content."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()
    if ext == '.csv':
        return parse_csv(filepath)
    elif ext == '.json':
        return parse_json(filepath)
    elif ext == '.html':
        return parse_html(filepath)
    elif ext == '.txt':
        return parse_txt(filepath)
    elif ext == '.md':
        return parse_markdown(filepath)
    else:
        raise ValueError(f"Unknown file type: {ext}")

def parse_csv(filepath):
    """Parses a CSV file."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def parse_json(filepath):
    """Parses a JSON file."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        return json.load(f)

def parse_html(filepath):
    """Parses an HTML file and extracts links."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href="([^"]+)"', content)
    return [{'url': link} for link in links]

def parse_txt(filepath):
    """Parses a TXT file and extracts URLs."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    return [{'url': line.strip()} for line in lines if line.strip()]

def format_for_hoarder(data, list_name):
    """Formats data for Hoarder."""
    formatted = []
    now = int(time.time())
    for entry in data:
        url = str(entry.get('url', '') or '')
        title = str(entry.get('title', '') or '')
        description = str(entry.get('description', '') or '')
        tags = entry.get('tags', [])
        list_str = str(list_name or '')
        # Guarantee all fields are present and strings
        if url and validate_url(url):
            formatted.append({
                'url': url,
                'title': title,
                'description': description,
                'tags': tags if isinstance(tags, list) else [],
                'list': list_str,
                'createdAt': now
            })
    return formatted

def preview_data(data):
    """Shows a preview of the data."""
    print("\n--- Preview of the data ---")
    for i, entry in enumerate(data[:10], start=1):
        print(f"{i}. URL: {entry['url']}")
        print(f"   Titel: {entry.get('title', 'N/A')}")
        print(f"   Beschreibung: {entry.get('description', 'N/A')}")
        print(f"   Tags: {', '.join(entry.get('tags', []))}")
        print(f"   Liste: {entry.get('list', 'N/A')}")
    if len(data) > 10:
        print(f"... und {len(data) - 10} more Entries.")

def save_to_json(data, output_file):
    """Saves the data in a JSON file."""
    # Wrap the data array in an object with "bookmarks" key
    output_data = {"bookmarks": data}
    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"\nData successfully in {output_file} saved.")

def main():
    filepath = input("Enter the path to the file: ").strip()
    list_name = input("Enter the name of the Hoarder list: ").strip()
    
    try:
        data = parse_file(filepath)
        formatted_data = format_for_hoarder(data, list_name)
        preview_data(formatted_data)
        
        if input("\nWould you like to export the data? (yes/no): ").strip().lower() in ['yes', 'y', 'ja', 'j']:
            output_file = input("Enter the name of the output file (e.g. output.json): ").strip()
            save_to_json(formatted_data, output_file)
        else:
            print("Export canceled.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
