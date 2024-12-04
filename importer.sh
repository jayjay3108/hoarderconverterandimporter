#!/bin/bash

# Function for validating URLs
validate_url() {
    curl -Is --max-time 5 "$1" | head -n 1 | grep -q "200 OK"
}

# Function for parsing files
parse_file() {
    case "$1" in
        *.csv)
            awk -F',' 'NR > 1 {print "{\"url\": \"" $1 "\", \"title\": \"" $2 "\", \"description\": \"" $3 "\"},"}' "$1"
            ;;
        *.json)
            jq -c '.[] | {url: .url, title: .title, description: .description}' "$1"
            ;;
        *.html)
            grep -oP '(?<=href=")[^"]*' "$1" | awk '{print "{\"url\": \"" $1 "\"},"}'
            ;;
        *.txt)
            awk '{print "{\"url\": \"" $0 "\"},"}' "$1"
            ;;
        *)
            echo "Unbekannter Dateityp: $1"
            exit 1
            ;;
    esac
}

# Main logic
read -p "Gib den Pfad zur Datei ein: " filepath
read -p "Gib den Namen der Hoarder-Liste ein: " list_name

if [ ! -f "$filepath" ]; then
    echo "Datei nicht gefunden!"
    exit 1
fi

# Extract and validate links from file
output="["
while read -r line; do
    url=$(echo "$line" | jq -r '.url')
    if validate_url "$url"; then
        title=$(echo "$line" | jq -r '.title // ""')
        description=$(echo "$line" | jq -r '.description // ""')
        output+="{\"url\": \"$url\", \"title\": \"$title\", \"description\": \"$description\", \"list\": \"$list_name\"},"
    fi
done < <(parse_file "$filepath")

# Closure of the JSON structure
output="${output%,}]"

# Preview of the data
echo -e "\n--- Vorschau der Daten ---"
echo "$output" | jq '.' | head -n 20

read -p "Möchtest du die Daten exportieren? (ja/nein): " confirm
if [[ "$confirm" =~ ^[Jj]a$ ]]; then
    read -p "Gib den Namen der Ausgabedatei ein (z.B. output.json): " output_file
    echo "$output" > "$output_file"
    echo "Daten erfolgreich in $output_file gespeichert."
else
    echo "Export abgebrochen."
fi