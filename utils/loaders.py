from dotenv import dotenv_values
from typing import Dict
from pathlib import Path
import sys
 
def load_env_vars(env_path: str) -> Dict[str, str | None]:
    return dotenv_values(env_path)


def load_bookmarks():
    HOME_DIR = Path.home()
    PLATFORM = sys.platform
    bookmarks_path = {"win32" : HOME_DIR/"AppData/Local/Google/Chrome/User Data/Default/Bookmarks"}
    return bookmarks_path[PLATFORM]

def load_output_dir(file_name: str) -> Path:
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)
    file_path = output_dir / file_name
    return file_path