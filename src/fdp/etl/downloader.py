# src/fdp/etl/downloader.py
from pathlib import Path

def download_sample(ids, out_dir="data/raw"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for i in ids:
        Path(out_dir, f"{i}.pdf").write_bytes(b"%PDF-1.4\n%EOF")
    return True

# src/fdp/etl/parser.py
def parse_pdf(path: str) -> dict:
    # stub values for now
    return {"eo_number": None, "title": "", "signed_date": None, "body_text": ""}
