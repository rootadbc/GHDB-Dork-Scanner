# Key Differences Between `ghdb_api_v1_scraper.py` and `ghdb_api_scraper.py`

**Main Takeaway:**  
The primary distinction lies in how each script extracts the “dork” strings from the Exploit-DB Google Hacking Database API response:  
- **`ghdb_api_v1_scraper.py`** directly parses the JSON payload to pull out dork values.  
- **`ghdb_api_scraper.py`** uses BeautifulSoup to parse HTML contained within a JSON field.  

***

## 1. Dependencies
- **API v1 scraper** (`ghdb_api_v1_scraper.py`) relies only on:
  - `requests`
  - `csv`
  - `time`

- **Generic scraper** (`ghdb_api_scraper.py`) adds:
  - `bs4` (BeautifulSoup)
  
***

## 2. Data Extraction Logic

### ghdb_api_v1_scraper.py
- Fetches JSON from the API endpoint (`/google-hacking-database`) with datatable parameters.
- Reads the `data` array of rows.
- For each row:
  - If it’s a dictionary, attempts to get the dork from `row.get("1")`, `row.get(1)`, or `row.get("dork")`.
  - If it’s a list or tuple, takes the second element (`row`).[1]
- Strips whitespace and collects into a Python set for uniqueness.
- Includes a one-time “DEBUG sample row” print on the first page of results.

### ghdb_api_scraper.py
- Fetches the same JSON payload.
- For each row:
  - Extracts the HTML snippet from the `url_title` field.
  - Uses BeautifulSoup to parse that HTML and pull out the anchor text.
  - Adds the cleaned text (the dork) to the set.

***

## 3. Debugging Output
- **v1 scraper** prints a debug sample of the very first row fetched.  
- **Generic scraper** prints only the count of rows fetched per offset.

***

## 4. Code Paths and Branching
- **API v1 scraper** has branching logic to handle rows represented either as:
  - A dictionary with numeric or string keys.
  - A list/tuple structure.
- **Generic scraper** assumes each row provides an HTML snippet under `url_title` and unconditionally passes it through BeautifulSoup.

***

## 5. Installation and Runtime Considerations
- To run **v1**, no additional libraries beyond the standard library and `requests` are required.
- To run **generic**, ensure `beautifulsoup4` is installed (e.g., `pip install beautifulsoup4`).

***

In summary, choose **`ghdb_api_v1_scraper.py`** for simpler, direct JSON‐based extraction when the API schema is stable. Use **`ghdb_api_scraper.py`** if you need to parse HTML link text (e.g., if the JSON schema changes or embeds markup).

[1](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/93916732/882c35d7-9415-4aff-831b-eb9851732090/ghdb_api_v1_scraper.py)
[2](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/93916732/d486fd9b-6981-4cf3-9a86-77ad92f0ed9c/ghdb_api_scraper.py)
