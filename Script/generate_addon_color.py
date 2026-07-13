import json
import re

ADDONINFO_PATH = "../../TownOfHost-Pko/Roles/AddOns/Addoninfo.cs"
OUTPUT_PATH = "role_color.json"

COLOR_DICT_PATTERN = re.compile(r"\{\s*CustomRoles\.(\w+)\s*,\s*\"(#[0-9A-Fa-f]{6})\"\s*\}")

with open(ADDONINFO_PATH, encoding="utf-8") as f:
    addoninfo = f.read()

colors = dict(COLOR_DICT_PATTERN.findall(addoninfo))

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(colors, f, ensure_ascii=False, indent=2)
