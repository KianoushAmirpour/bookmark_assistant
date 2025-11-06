import json
from typing import Dict, Any, List
from pathlib import Path
import random
from datetime import datetime, timedelta

def load_extract_bookmarks(bookmark_path: str) -> List[Dict[str, Any]]:
    """
    Load Chrome bookmarks from the specified file path and returns their contents as a JSON object.

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
                            The file might already exist.
        data (dict[str, Any]): The dictionary to serialize and save as JSON.
    """
    
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with output_dir.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def load_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Load a JSON file and returns its contents as a dictionary.

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
        
def load_json_file_recency(file_path: Path) -> Dict[str, Any]:
    """
    Load a JSON file and returns its contents as a dictionary.

    Args:
        file_path (Path): The path to the JSON file.

    Returns:
        dict: The contents of the JSON file as a dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for item in data:
        item.pop("name", None)
        item.pop("date_last_used", None)
    return data[:20]
    
def write_markdown_file(output_path: Path, content: str):
    """
    Writes content to a markdown file.

    This function ensures the parent directory exists before writing.
    If the file already exists, it will be overwritten.

    Args:
        output_path (Path): The path where the markdown file will be written.
        content (str): The content to write to the markdown file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(content)
        
def convert_webkit_timestamp(data:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    
    """
    Converts the 'date_added' field in a list of bookmark items from WebKit timestamps 
    (microseconds since January 1, 1601 UTC) to human-readable datetime strings.

    Args:
        data (List[Dict[str, Any]]): 
            A list of dictionaries representing bookmark items. 
            Each dictionary must contain a 'date_added' field with a WebKit timestamp.

    Returns:
        List[Dict[str, Any]]: 
            The same list with the 'date_added' fields converted to formatted 
            datetime.
    """
    EPOCH_START = datetime(1601, 1, 1)
    for item in data:
        seconds = int(item["date_added"]) / 1_000_000
        item["date_added"] = EPOCH_START + timedelta(seconds=seconds)
    return data

def sort_by_datetime_key(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sorts a list of dictionaries based on the 'date_added' key, 
    assuming its value is a datetime object or a comparable type.

    Args:
        data (List[Dict[str, Any]]): 
            A list of dictionaries, each containing a 'date_added' field 
            representing a datetime or timestamp value.

    Returns:
        List[Dict[str, Any]]: 
            A new list of dictionaries sorted in ascending order 
            (oldest first) by the 'date_added' field.
    """
    sorted_data = sorted(data, key=lambda x: x["date_added"], reverse=False)
    return sorted_data

def format_datetime(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Formats the 'date_added' field in each dictionary as a string 
    in the "YYYY-MM-DD" format.

    Args:
        data (List[Dict[str, Any]]): 
            A list of dictionaries, each containing a 'date_added' key 
            with a datetime object as its value.

    Returns:
        List[Dict[str, Any]]: 
            The same list of dictionaries with the 'date_added' field 
            converted to a string formatted as "%Y-%m-%d".
    """
    for item in data:
        item["date_added"] = datetime.fromisoformat(item["date_added"]).strftime("%Y-%m-%d")
    return data