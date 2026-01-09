import json
from pathlib import Path
from dateutil.parser import parse
import pandas as pd

def deep_get(d, path, default=None):
    cur = d
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur

def parse_date(x):
    if not x:
        return None
    if isinstance(x, dict):
        x = x.get("date")
    if not x:
        return None
    try:
        return parse(str(x)).date()
    except Exception:
        return None

def main():
    raw_path = Path("data/raw/t2d_studies_raw.json")
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)

    studies = json.loads(raw_path.read_text(encoding="utf-8"))

    rows = []
    for s in studies:
        ps = s.get("protocolSection", {}) or {}

        nct_id = deep_get(ps, ["identificationModule", "nctId"])
        if not nct_id:
            continue

        rows.append({
            "nct_id": nct_id,
            "brief_title": deep_get(ps, ["identificationModule", "briefTitle"]),
            "official_title": deep_get(ps, ["identificationModule", "officialTitle"]),
            "overall_status": deep_get(ps, ["statusModule", "overallStatus"]),
            "study_type": deep_get(ps, ["designModule", "studyType"]),
            "start_date": parse_date(deep_get(ps, ["statusModule", "startDateStruct"])),
            "completion_date": parse_date(deep_get(ps, ["statusModule", "completionDateStruct"])),
            "enrollment_count": deep_get(ps, ["designModule", "enrollmentInfo", "count"]),
            "lead_sponsor": deep_get(ps, ["sponsorsModule", "leadSponsor", "name"]),
            "last_update_posted_date": parse_date(deep_get(ps, ["statusModule", "lastUpdatePostDateStruct"])),
            "has_results": bool(s.get("hasResults")),
        })

    df = pd.DataFrame(rows).drop_duplicates(subset=["nct_id"])
    # enrollment_count cleanup
    df["enrollment_count"] = pd.to_numeric(df["enrollment_count"], errors="coerce").astype("Int64")

    out_path = out_dir / "trials.csv"
    df.to_csv(out_path, index=False)
    print("Wrote:", out_path, "rows:", len(df))

if __name__ == "__main__":
    main()
