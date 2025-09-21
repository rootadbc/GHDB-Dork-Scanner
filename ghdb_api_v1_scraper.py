import requests, csv, time

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
    first = True

    for offset in range(0, total, per_page):
        params = {"datatable": "true", "start": offset, "length": per_page}
        resp = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        json_data = resp.json()
        batch = json_data.get("data", [])
        print(f"Fetched {len(batch)} rows at offset {offset}")

        if first and batch:
            print("DEBUG sample row:", batch[0])
            first = False

        for row in batch:
            # Try numeric key first, then string key
            dork = None
            if isinstance(row, dict):
                dork = row.get("1") or row.get(1) or row.get("dork")
            elif isinstance(row, (list, tuple)) and len(row) > 1:
                dork = row[1]
            if dork:
                dorks.add(dork.strip())
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
