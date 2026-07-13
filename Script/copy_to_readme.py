import shutil

SOURCE_PATH = "role_descriptions.md"
DEST_PATH = "../README.md"

shutil.copyfile(SOURCE_PATH, DEST_PATH)
