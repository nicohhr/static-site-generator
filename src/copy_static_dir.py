import logging
import os
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent

def copy_static(dst_path:str = "public") -> None:
    # Define delete directory
    shutil.rmtree(BASE_DIR / dst_path, ignore_errors=True)

    # Recrearte dir
    os.mkdir(BASE_DIR / dst_path)

    # List files
    copy_files_tree(BASE_DIR / "static", BASE_DIR / dst_path)

def copy_files_tree(current_path: Path, destination: Path) -> None:

    # List files and dirs
    list_dir = os.listdir(current_path)

    for item in list_dir:
        if os.path.isfile(current_path / item):
            # Copy file to destination
            shutil.copy(current_path / item, destination)
            logger.warning("Copied: " + str(destination) + "/" + item)
        else:
            # Create directory
            os.mkdir(destination / item)
            # Calls it own function again
            copy_files_tree(current_path / item, destination / item)
