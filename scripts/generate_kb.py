import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def generate():
    with (ROOT / "knowledge-base/it-knowledge-base.csv").open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f, delimiter=";"))
    ids = [row["article_id"] for row in rows]
    if len(ids) != len(set(ids)) or not all(re.fullmatch(r"KB-\d{3}", i) for i in ids):
        raise ValueError("Invalid article IDs")
    target = ROOT / "knowledge-base/documents"
    target.mkdir(exist_ok=True)
    for row in rows:
        text = f"# {row['article_id']} — {row['title']}\n\n"
        for key, value in row.items():
            if key not in {"article_id", "title"}:
                text += f"## {key}\n\n{value.replace(' | ', chr(10) + '- ')}\n\n"
        (target / (row["article_id"] + ".md")).write_text(
            text.rstrip("\n") + "\n",
            encoding="utf-8",
        )
    stale = set(target.glob("KB-*.md")) - {target / (i + ".md") for i in ids}
    if stale:
        raise ValueError("Stale generated documents; review and remove explicitly")
    print(f"Generated {len(rows)} documents")

if __name__ == "__main__":
    generate()
