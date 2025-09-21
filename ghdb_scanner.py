import csv
import time
import logging
import requests
from datetime import datetime
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GHDB_Scanner")

def load_ghdb_dorks(csv_path="ghdb_dorks.csv"):
    dorks = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pattern = row["dork"].strip()
            if pattern:
                dorks.append(pattern)
    logger.info(f"Loaded {len(dorks)} dorks from {csv_path}")
    return dorks

class GoogleDorkScanner:
    def __init__(self, target, dorks, max_results=20, delay=1.0):
        parsed = urlparse(target)
        self.target = parsed.netloc or target
        self.dorks = dorks
        self.max_results = max_results
        self.delay = delay
        self.findings = []

    def scan(self):
        logger.info(f"Starting scan on {self.target} with {len(self.dorks)} dorks")
        with DDGS() as ddgs:
            for dork in self.dorks:
                query = f"site:{self.target} {dork}"
                try:
                    results = list(ddgs.text(query, max_results=self.max_results))
                except Exception as e:
                    logger.error(f"Search failed for '{dork}': {e}")
                    continue

                for item in results:
                    url = item.get("href", "")
                    if urlparse(url).netloc.endswith(self.target):
                        self.findings.append((dork, url))
                        logger.warning(f"[VULN] {dork} → {url}")
                time.sleep(self.delay)
        logger.info("Scan complete.")

    def save_results(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = f"{self.target.replace('.', '_')}_scan_{ts}.csv"
        with open(fname, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["dork", "matched_url"])
            writer.writerows(self.findings)
        logger.info(f"Results saved to {fname}")

if __name__ == "__main__":
    # 1) Load dorks
    ghdb_list = load_ghdb_dorks("ghdb_dorks.csv")
    # 2) Set target
    target = "http://www.fifi.org"
    # 3) Run scanner
    scanner = GoogleDorkScanner(target, ghdb_list, max_results=20, delay=1.0)
    scanner.scan()
    # 4) Save findings
    scanner.save_results()
