from copy_static_dir import copy_static
from generate_page import generate_page

def main():
    # Copy from static to public
    copy_static()

    # Generate page to public/index.html from index.md using template.html
    generate_page()

if __name__ == "__main__":
    main()
