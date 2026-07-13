import json
import re
from pathlib import Path

PROJECT_DIR = Path("../../TownOfHost-Pko")
OUTPUT_PATH = "role_source_color.json"

CALL_START_PATTERN = re.compile(r"SimpleRoleInfo\.(Create|CreateForVanilla)\s*\(")
CUSTOM_ROLES_PATTERN = re.compile(r"CustomRoles\.(\w+)")
COLOR_PATTERN = re.compile(r'"(#[0-9A-Fa-f]{6})"')
CUSTOM_ROLE_TYPE_PATTERN = re.compile(r"CustomRoleTypes\.(\w+)")
BASE_ROLE_TYPE_PATTERN = re.compile(r"RoleTypes\.(\w+)")

# mirrors the `baseRoleType switch` inside SimpleRoleInfo.CreateForVanilla
VANILLA_ROLE_TYPE_MAP = {
    "Engineer": "Crewmate",
    "Scientist": "Crewmate",
    "Tracker": "Crewmate",
    "Noisemaker": "Crewmate",
    "Detective": "Crewmate",
    "GuardianAngel": "Crewmate",
    "Impostor": "Impostor",
    "Shapeshifter": "Impostor",
    "Phantom": "Impostor",
    "Viper": "Impostor",
}

# mirrors the `colorCode == ""` fallback inside SimpleRoleInfo's constructor
DEFAULT_COLOR_BY_ROLE_TYPE = {
    "Impostor": "#ff1919",
    "Madmate": "#ff1919",
    "Crewmate": "#8cffff",
}


def default_color_for(custom_role_type):
    return DEFAULT_COLOR_BY_ROLE_TYPE.get(custom_role_type, "#ffffff")


def extract_balanced(text, open_paren_index):
    """Return the text between the '(' at open_paren_index and its matching ')'."""
    depth = 1
    i = open_paren_index + 1
    start = i
    while i < len(text) and depth > 0:
        if text[i] == "(":
            depth += 1
        elif text[i] == ")":
            depth -= 1
        i += 1
    return text[start : i - 1]


def find_role_colors(cs_text):
    results = {}
    for match in CALL_START_PATTERN.finditer(cs_text):
        call_kind = match.group(1)
        open_paren_index = match.end() - 1
        block = extract_balanced(cs_text, open_paren_index)

        if call_kind == "Create":
            # role name comes from the explicit CustomRoles.X argument, not typeof() --
            # some files (e.g. CandleLighter.cs) pass a mismatched typeof() by mistake
            roles_match = CUSTOM_ROLES_PATTERN.search(block)
            if not roles_match:
                continue
            role_name = roles_match.group(1)

            custom_role_type_match = CUSTOM_ROLE_TYPE_PATTERN.search(block)
            custom_role_type = custom_role_type_match.group(1) if custom_role_type_match else None
        else:  # CreateForVanilla: roleName and customRoleType are both derived from baseRoleType
            base_role_type_match = BASE_ROLE_TYPE_PATTERN.search(block)
            if not base_role_type_match:
                continue
            role_name = base_role_type_match.group(1)
            custom_role_type = VANILLA_ROLE_TYPE_MAP.get(role_name, "Crewmate")

        color_match = COLOR_PATTERN.search(block)
        results[role_name] = color_match.group(1) if color_match else default_color_for(custom_role_type)
    return results


role_colors = {}

for cs_path in sorted(PROJECT_DIR.rglob("*.cs")):
    text = cs_path.read_text(encoding="utf-8-sig")
    role_colors.update(find_role_colors(text))

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(role_colors, f, ensure_ascii=False, indent=2)

print(f"{len(role_colors)} roles extracted")
