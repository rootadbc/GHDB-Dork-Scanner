# GHDB Dork Scanner

A Python tool that fetches GHDB dorks and runs site-restricted searches to uncover potential exposures on your target website.

## Prerequisites
- Python 3.8+  
- pip  
- Internet access  

## Installation
1. Clone the repo and enter its folder:  
   ```bash
   git clone https://github.com/rootadbc/ghdb-dork-scanner.git
   cd ghdb-dork-scanner
   ```
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
   (*requests, beautifulsoup4, duckduckgo_search*)

## Quick Start
1. Download all GHDB dorks into `ghdb_dorks.csv`:  
   ```bash
   python ghdb_api_scraper.py
   ```
2. Scan your site for leaks:  
   ```bash
   python ghdb_scanner.py \
     --target https://example.com \
     --dorks ghdb_dorks.csv \
     --max-results 20 \
     --delay 1.0
   ```
   - `--target` (site to audit)  
   - `--dorks` (path to CSV; default `ghdb_dorks.csv`)  
   - `--max-results` (results per dork; default 20)  
   - `--delay` (seconds between queries; default 1.0)  

## Output
Results are saved as `<hostname>_scan_<YYYYMMDD_HHMMSS>.csv` with two columns: `dork,matched_url`.

## Ethical Use
Only run against systems you have permission to test. Unauthorized scanning is prohibited.  

## License
MIT License. See `LICENSE`.
