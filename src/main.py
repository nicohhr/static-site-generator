from copy_static_dir import copy_static
from generate_page import *
from sys import argv

def main():
    # Reading script arguments
    base_path = None if len(argv) == 1 else argv[1]
    print(base_path)

    # Copy from static to public
    copy_static()

    # Generate page to public/index.html from index.md using template.html
    generate_pages_recursive()

if __name__ == "__main__":
    main()
