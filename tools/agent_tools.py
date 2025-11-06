import json
from typing import Dict, Any, List
from pathlib import Path
import random

def load_extract_bookmarks(bookmark_path: str) -> List[Dict[str, Any]]:
    """
    Load Chrome bookmarks from the specified file path and return their contents as a JSON object.

    Args:
        bookmark_path (str): The full path to the Chrome bookmarks file.

    Returns:
        dict: A dictionary representing the bookmark data, with 'sync_metadata' and 'version' removed if present.
    """
    with open(bookmark_path, "r", encoding="utf-8") as f:
        bookmark_data_dict = json.load(f)
    
    bookmark_data_dict.pop("sync_metadata", None)
    bookmark_data_dict.pop("version", None)
    
    childrens = bookmark_data_dict["roots"]["bookmark_bar"]["children"]
    cleaned_bookmarks = []
    for items in childrens:
        if "children" in items.keys():
            for bookmark in items["children"]:
                bookmark.pop("guid", None)
                bookmark.pop("id", None)
                bookmark.pop("meta_info", None)
                bookmark.pop("type", None)
                cleaned_bookmarks.append(bookmark)
        else: 
            continue
    random.shuffle(cleaned_bookmarks)
    return cleaned_bookmarks
    
def write_extracted_bookmarks(output_dir: Path, data: List[Dict[str, Any]]):
    """
    Write a dictionary of extracted bookmarks to a JSON file.

    This function ensures the parent directory exists before writing.
    If the file already exists, it will be overwritten.

    Args:
        output_path (Path): The path where the JSON file will be written.
                            The file may or may not already exist.
        data (dict[str, Any]): The dictionary to serialize and save as JSON.

    Raises:
        OSError: If there is an issue creating directories or writing the file.
        TypeError: If `data` is not JSON-serializable.
    """
    
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with output_dir.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Load a JSON file and return its contents as a dictionary.

    Args:
        file_path (Path): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        item.pop("date_added", None)
        item.pop("date_last_used", None)
    return data[:200]
        # return json.load(f)
    
def write_markdown_file(output_path: Path, content: str):
    """
    Write content to a markdown file.

    This function ensures the parent directory exists before writing.
    If the file already exists, it will be overwritten.

    Args:
        output_path (Path): The path where the markdown file will be written.
        content (str): The content to write to the markdown file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)