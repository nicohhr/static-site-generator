import logging
from operator import lshift
import os
from pathlib import Path
from posix import listdir
import shutil
from sys import path

logger = logging.getLogger(__name__)

def copy_static() -> None:
    # Define delete directory
    shutil.rmtree(Path.cwd() / "public")

    # Recrearte dir
    os.mkdir("public")

    # List files
    copy_files_tree(Path.cwd() / "static", Path.cwd() / "public")

def copy_files_tree(current_path: Path, destination: Path) -> None:
    # List files and dirs
    list_dir = os.listdir(current_path)

    for item in list_dir:
        if os.path.isfile(current_path / item):
            # Copy file to destination
            shutil.copy(current_path / item, destination)
            logger.warning("Copied:" + item)
        else:
            # Create directory
            os.mkdir(destination / item)
            # Calls it own function again
            copy_files_tree(current_path / item, destination / item)

def main():
    copy_static()

if __name__ == "__main__":
    main()
