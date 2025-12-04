"""
Storage utilities for file caching, S3, or other storage backends
Optional module for future enhancements
"""
from typing import Optional
from pathlib import Path


class StorageService:
    """Storage service for managing transcript files and outputs"""

    def __init__(self, storage_path: str = "./storage"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

    def save_file(self, filename: str, content: bytes) -> str:
        """
        Save a file to local storage.

        Args:
            filename: Name of the file
            content: Binary content

        Returns:
            Path to saved file
        """
        file_path = self.storage_path / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        return str(file_path)

    def read_file(self, filename: str) -> Optional[bytes]:
        """
        Read a file from local storage.

        Args:
            filename: Name of the file

        Returns:
            File content as bytes, or None if not found
        """
        file_path = self.storage_path / filename
        if not file_path.exists():
            return None

        with open(file_path, 'rb') as f:
            return f.read()

    def delete_file(self, filename: str) -> bool:
        """
        Delete a file from local storage.

        Args:
            filename: Name of the file

        Returns:
            True if deleted, False if not found
        """
        file_path = self.storage_path / filename
        if file_path.exists():
            file_path.unlink()
            return True
        return False


# Future: Add S3StorageService, AzureBlobStorageService, etc.

