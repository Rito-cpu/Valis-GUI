import os
import mimetypes
import pathlib

from typing import Optional


def is_json_file(filepath: pathlib.Path) -> bool:
    """Check if the file has a JSON mime type."""
    mime_type, _ = mimetypes.guess_type(filepath)

    return mime_type == "application/json"

def is_valid_json_file(filepath: pathlib.Path) -> bool:
    """Check if the file is a valid JSON file."""

    return is_json_file(filepath) and is_existing_path(filepath)

def is_excel_file(filepath: pathlib.Path) -> bool:
    """Check if the file has an Excel mime type."""
    mime_type, _ = mimetypes.guess_type(filepath)
    target_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return mime_type == target_type

def is_valid_excel_file(filepath: pathlib.Path) -> bool:
    """Check if the file is a valid Excel file."""

    return is_excel_file(filepath) and filepath.exists()

def is_blank_line(line: Optional[str]) -> bool:
    """Check if the line is blank or None."""

    return line is None or not line.strip()

def is_existing_dir(path: Optional[pathlib.Path]) -> bool:
    return path.is_dir() if path else False

def is_existing_path(path: Optional[pathlib.Path]) -> bool:
    return path.exists() if path else False
