import requests, csv, time
from bs4 import BeautifulSoup

OUTPUT_FILE = "ghdb_dorks.csv"
BASE_URL    = "https://www.exploit-db.com/google-hacking-database"
HEADERS     = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}

def fetch_ghdb_dorks_via_api():
    dorks = set()
    per_page = 120
    total = 7944

    for offset in range(0, total, per_page):
        params = {"datatable": "true", "start": offset, "length": per_page}
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        json_data = resp.json()
        batch = json_data.get("data", [])
        print(f"Fetched {len(batch)} rows at offset {offset}")

        for row in batch:
            html_link = row.get("url_title", "")
            # Parse out the anchor text
            soup = BeautifulSoup(html_link, "html.parser")
            dork = soup.get_text(strip=True)
            if dork:
                dorks.add(dork)

        time.sleep(0.2)

    return sorted(dorks)

def write_csv(dorks, path=OUTPUT_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["dork"])
        for d in dorks:
            writer.writerow([d])
    print(f"Wrote {len(dorks)} unique dorks to {path}")

if __name__ == "__main__":
    all_dorks = fetch_ghdb_dorks_via_api()
    write_csv(all_dorks)
