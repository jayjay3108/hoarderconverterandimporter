import os
import csv
import json
import re
import html.parser
import mimetypes
import requests

def validate_url(url):
    """Prüft, ob eine URL gültig ist und erreichbar."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def parse_file(filepath):
    """Erkennt Dateityp und extrahiert Inhalte."""
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
    else:
        raise ValueError(f"Unbekannter Dateityp: {ext}")

def parse_csv(filepath):
    """Parst eine CSV-Datei."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for row in reader]

def parse_json(filepath):
    """Parst eine JSON-Datei."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        return json.load(f)

def parse_html(filepath):
    """Parst eine HTML-Datei und extrahiert Links."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        content = f.read()
    links = re.findall(r'href="([^"]+)"', content)
    return [{'url': link} for link in links]

def parse_txt(filepath):
    """Parst eine TXT-Datei und extrahiert URLs."""
    with open(filepath, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    return [{'url': line.strip()} for line in lines if line.strip()]

def format_for_hoarder(data, list_name):
    """Formatiert Daten für Hoarder."""
    formatted = []
    for entry in data:
        if 'url' in entry and validate_url(entry['url']):
            formatted.append({
                'url': entry['url'],
                'title': entry.get('title', ''),
                'description': entry.get('description', ''),
                'tags': entry.get('tags', []),
                'list': list_name
            })
    return formatted

def preview_data(data):
    """Zeigt eine Vorschau der Daten."""
    print("\n--- Vorschau der Daten ---")
    for i, entry in enumerate(data[:10], start=1):
        print(f"{i}. URL: {entry['url']}")
        print(f"   Titel: {entry.get('title', 'N/A')}")
        print(f"   Beschreibung: {entry.get('description', 'N/A')}")
        print(f"   Tags: {', '.join(entry.get('tags', []))}")
        print(f"   Liste: {entry.get('list', 'N/A')}")
    if len(data) > 10:
        print(f"... und {len(data) - 10} weitere Einträge.")

def save_to_json(data, output_file):
    """Speichert die Daten in eine JSON-Datei."""
    with open(output_file, mode='w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\nDaten erfolgreich in {output_file} gespeichert.")

def main():
    filepath = input("Gib den Pfad zur Datei ein: ").strip()
    list_name = input("Gib den Namen der Hoarder-Liste ein: ").strip()
    
    try:
        data = parse_file(filepath)
        formatted_data = format_for_hoarder(data, list_name)
        preview_data(formatted_data)
        
        if input("\nMöchtest du die Daten exportieren? (ja/nein): ").strip().lower() == 'ja':
            output_file = input("Gib den Namen der Ausgabedatei ein (z.B. output.json): ").strip()
            save_to_json(formatted_data, output_file)
        else:
            print("Export abgebrochen.")
    except Exception as e:
        print(f"Fehler: {e}")

if __name__ == "__main__":
    main()
