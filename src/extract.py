import json
import time
from pathlib import Path
import requests

BASE = "https://clinicaltrials.gov/api/v2/studies"

def fetch_all(condition: str, page_size: int = 1000):
    params = {"query.cond": condition, "pageSize": page_size, "countTotal": "true"}
    all_studies = []
    page_token = None
    page = 1

    while True:
        if page_token:
            params["pageToken"] = page_token

        r = requests.get(BASE, params=params, timeout=60)
        r.raise_for_status()
        data = r.json()

        studies = data.get("studies", [])
        all_studies.extend(studies)

        print(f"page {page} -> got {len(studies)} (total {len(all_studies)})")

        page_token = data.get("nextPageToken")
        if not page_token or len(studies) == 0:
            break

        page += 1
        time.sleep(0.2)

    return all_studies

def main():
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    studies = fetch_all("Type 2 Diabetes Mellitus")
    (out_dir / "t2d_studies_raw.json").write_text(json.dumps(studies), encoding="utf-8")
    print("Saved:", out_dir / "t2d_studies_raw.json")

if __name__ == "__main__":
    main()
