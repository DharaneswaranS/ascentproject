import os

def get_latest_version():
    versions = [f for f in os.listdir("outputs") if f.startswith("edited_")]
    return len(versions)

def save_new_version(text):
    version = get_latest_version() + 1
    path = f"outputs/edited_v{version}.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return path
def get_latest_edited_text():
    versions = sorted(
        [f for f in os.listdir("outputs") if f.startswith("edited_")]
    )
    if not versions:
        return None

    latest = versions[-1]
    with open(f"outputs/{latest}", "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

