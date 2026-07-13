import csv
import json
import re

CSV_PATH = "../../TownOfHost-Pko/Resources/string.csv"
OUTPUT_PATH = "role_descriptions.json"

# a section tag is a single "#" (not "##") followed by either a space + text
# (`# HideAndSeek`, `# バニラ役職`) or, with no space, non-ascii text (`#コンビネーション役職`).
# Ascii id-style markers with no space (`#ImpostorName`, `#5 ...`) are not tags.
TAG_PATTERN = re.compile(r"^#(.*)$")

with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.reader(f))

# index rows by their id (column 1) for InfoLong / Info lookups
rows_by_id = {row[0]: row for row in rows if row and row[0]}

result = {}
current_tag = None

for line_number, row in enumerate(rows[:390], start=1):  # lines 1-390 (1-indexed)
    if row and not row[0].startswith("##"):
        match = TAG_PATTERN.match(row[0])
        if match:
            content = match.group(1)
            if content.startswith(" ") or (content and not content[0].isascii()):
                current_tag = content.strip()

    if line_number < 11 or len(row) < 3:
        continue

    role = row[0]
    role_name = row[2]

    role_search_long = role + "InfoLong"
    role_search_short = role + "Info"

    long_row = rows_by_id.get(role_search_long)
    short_row = rows_by_id.get(role_search_short)

    role_description_long = long_row[2] if long_row and len(long_row) > 2 else ""
    role_description_short = short_row[2] if short_row and len(short_row) > 2 else ""

    result[role] = {
        "id": line_number,
        "name": role_name,
        "tag": current_tag,
        "long_description": role_description_long,
        "short_description": role_description_short,
    }

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
