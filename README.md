# hoarderconverterandimporter
Detects the file extension (HTML, CSV, JSON, TXT) automatically and converts it to JSON. Links validation and detection of title, tags and description.

---
---

How the python script works:

1. File type recognition: Supports HTML, CSV, JSON and TXT.
2. Extract links: Depending on the file type, URLs and additional data such as title and description are processed.
3. Validation: URLs are checked to filter out invalid or inaccessible links.
4. Preview: The first 10 entries are displayed so that you can check the data.
5. Export: Saves the data as a JSON file that can be imported into Hoarder.

---
---

How the Bash script works:

1. File type detection: Uses the file extension to select the appropriate method (CSV, JSON, HTML, TXT).
2. Extract links: Uses awk, grep, or jq, depending on the file type.
3. URL validation: Checks accessibility of URLs with curl.
4. Preview: Shows a JSON preview of the first 20 entries with jq.
5. Export: Saves the data in a JSON file.

---

Prerequisites:

- Tools such as curl, jq, and awk must be installed.
