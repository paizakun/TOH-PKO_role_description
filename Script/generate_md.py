import json

INPUT_PATH = "role_descriptions.json"
OUTPUT_PATH = "role_descriptions.md"

with open(INPUT_PATH, encoding="utf-8") as f:
    roles = json.load(f)

lines = []
current_tag = None

for role, data in roles.items():
    tag = data.get("tag")
    if tag != current_tag:
        lines.append(f"# {tag}")
        lines.append("")
        current_tag = tag

    description = data.get("long_description") or data.get("short_description") or ""
    description = description.replace("\\n", "\n")

    lines.append(f"## {data.get('name')}")
    lines.append("")
    lines.append(description)
    lines.append("")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
