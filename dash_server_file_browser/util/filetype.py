from enum import Enum
from pathlib import Path
from typing import Union


class FileType(Enum):
    """Enum of different file types.

    This enum is used to categorize files based on their extensions.
    Each file type is associated with a specific icon class from Font Awesome.
    """

    FILE = "fa-file"
    """Fallback icon for unhandled file types."""
    FILE_AUDIO = "fa-file-audio"
    """Audio files."""
    FILE_CODE = "fa-file-code"
    """Source code files."""
    FILE_EXCEL = "fa-file-excel"
    """Excel files"""
    FILE_IMAGE = "fa-file-image"
    """Image files."""
    FILE_LINES = "fa-file-lines"
    """Text files."""
    FILE_PDF = "fa-file-pdf"
    """PDF files."""
    FILE_POWERPOINT = "fa-file-powerpoint"
    """PowerPoint files."""
    FILE_VIDEO = "fa-file-video"
    """Video files."""
    FILE_WORD = "fa-file-word"
    """Word files."""
    FILE_ZIP = "fa-file-zipper"
    """Archive files."""

    def __str__(self) -> str:
        """Return the string representation of the enum member."""
        return self.value


_EXTENSION_MAP: dict[str, FileType] = {
    ".mp3": FileType.FILE_AUDIO,
    ".wav": FileType.FILE_AUDIO,
    ".flac": FileType.FILE_AUDIO,
    ".py": FileType.FILE_CODE,
    ".js": FileType.FILE_CODE,
    ".json": FileType.FILE_CODE,
    ".ts": FileType.FILE_CODE,
    ".java": FileType.FILE_CODE,
    ".c": FileType.FILE_CODE,
    ".cpp": FileType.FILE_CODE,
    ".html": FileType.FILE_CODE,
    ".css": FileType.FILE_CODE,
    ".xls": FileType.FILE_EXCEL,
    ".xlsx": FileType.FILE_EXCEL,
    ".jpg": FileType.FILE_IMAGE,
    ".jpeg": FileType.FILE_IMAGE,
    ".png": FileType.FILE_IMAGE,
    ".gif": FileType.FILE_IMAGE,
    ".txt": FileType.FILE_LINES,
    ".csv": FileType.FILE_LINES,
    ".log": FileType.FILE_LINES,
    ".pdf": FileType.FILE_PDF,
    ".ppt": FileType.FILE_POWERPOINT,
    ".pptx": FileType.FILE_POWERPOINT,
    ".mp4": FileType.FILE_VIDEO,
    ".avi": FileType.FILE_VIDEO,
    ".mkv": FileType.FILE_VIDEO,
    ".doc": FileType.FILE_WORD,
    ".docx": FileType.FILE_WORD,
    ".zip": FileType.FILE_ZIP,
    ".tar": FileType.FILE_ZIP,
    ".gz": FileType.FILE_ZIP,
}


def get_file_type(file_name: Union[str, Path]) -> FileType:
    """Get the file type based on the file name.

    Args:
        file_name (Union[str, Path]): The name of the file.
    """
    if isinstance(file_name, str):
        file_name = Path(file_name)

    return _EXTENSION_MAP.get(file_name.suffix.lower(), FileType.FILE)
