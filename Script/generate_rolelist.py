import json
from collections import OrderedDict

INPUT_PATH = "role_descriptions.json"
OUTPUT_PATH = "Rolelist.txt"

with open(INPUT_PATH, encoding="utf-8") as f:
    roles = json.load(f)

groups = OrderedDict()
for data in roles.values():
    tag = data.get("tag")
    groups.setdefault(tag, []).append(data.get("name"))

lines = []
for tag, names in groups.items():
    lines.append(f"{tag}({len(names)}件)")
    for i, name in enumerate(names, start=1):
        lines.append(f"{i}. {name}")
    lines.append("")

lines.append(f"合計: {sum(len(names) for names in groups.values())}件")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
