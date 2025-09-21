# GHDB Dork Scanner

A Python-based tool for ethical hacking that automates retrieval of the Google Hacking Database (GHDB) dorks and performs site-restricted searches to identify potential exposures on a target website.

## Features

- Automatically fetch all **7,944** GHDB dorks via Exploit-DB’s DataTables JSON API  
- Parse and save dorks into a CSV (`ghdb_dorks.csv`)  
- Perform DuckDuckGo site-restricted searches for each dork  
- Record and export any matched URLs as a timestamped CSV  
- Configurable search rate, result limits, and target URL  

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Usage](#usage)  
  - [1. Fetch GHDB Dorks](#1-fetch-ghdb-dorks)  
  - [2. Run the Scanner](#2-run-the-scanner)  
- [Configuration](#configuration)  
- [Output](#output)  
- [Ethical Notice](#ethical-notice)  
- [License](#license)  

## Prerequisites

- Python 3.8+  
- pip  
- Internet connectivity

## Installation

1. Clone this repository  
   ```bash
   git clone https://github.com/rootadbc/ghdb-dork-scanner.git
   cd ghdb-dork-scanner
   ```

2. Install required Python packages  
   ```bash
   pip install -r requirements.txt
   ```

   **requirements.txt**:
   ```
   requests
   beautifulsoup4
   duckduckgo_search
   ```

## Usage

### 1. Fetch GHDB Dorks

Use the API scraper to retrieve the full GHDB list and save to CSV:

```bash
python ghdb_api_scraper.py
```

- Iterates in 120-entry batches via `?datatable=true&start=<offset>&length=120`  
- Parses JSON `url_title` HTML fragments for dork text  
- Outputs `ghdb_dorks.csv` containing a header row and all unique dorks  

### 2. Run the Scanner

Load the CSV dorks and scan a target domain:

```bash
python ghdb_scanner.py --target https://example.com \
                       --dorks ghdb_dorks.csv \
                       --max-results 20 \
                       --delay 1.0
```

Options:

- `--target` (required): Base URL to audit  
- `--dorks`: Path to the GHDB CSV (defaults to `ghdb_dorks.csv`)  
- `--max-results`: Max search results per dork (default 20)  
- `--delay`: Delay (seconds) between queries (default 1.0)

Example:

```bash
python ghdb_scanner.py --target https://www.example.com \
                       --dorks ghdb_dorks.csv \
                       --max-results 10 \
                       --delay 0.5
```

## Configuration

Both scripts define constants at the top:

- **API scraper**  
  - `BASE_URL`: GHDB page URL  
  - `OUTPUT_FILE`: CSV path  
  - `HEADERS`: User-Agent and AJAX headers  

- **Scanner**  
  - `DDGS` parameters (`region`, `safesearch`)  
  - CSV output naming format uses `<hostname>_scan_<timestamp>.csv`

Adjust these values directly or extend the scripts to accept additional command-line flags.

## Output

- **ghdb_dorks.csv**:  
  ```
  dork
  site:github.com "BEGIN OPENSSH PRIVATE KEY"
  ext:nix "BEGIN OPENSSH PRIVATE KEY"
  inurl:home.htm intitle:1766
  …
  ```
- **<target>_scan_<YYYYMMDD_HHMMSS>.csv**:  
  ```
  dork,matched_url
  site:github.com "BEGIN OPENSSH PRIVATE KEY",https://example.com/path/to/key
  …
  ```

## Ethical Notice

This tool is intended for authorized penetration testing and security auditing only. Do **not** use it on systems without explicit permission. Abuse may violate terms of service or legal regulations.

## License

This project is released under the MIT License.  
See [LICENSE](LICENSE) for details.
