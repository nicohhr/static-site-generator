import os
from pathlib import Path
from posix import mkdir
import re

from blocknode import *
from markdown_utils import *

from_base_path = "content/"
dest_base_path = "public/"
from_path = "content/index.md"
dest_path = "public/index.html"
template_path = "template.html"

def generate_pages_recursive():
    crawl_for_md(Path(from_base_path), Path(dest_base_path))

def crawl_for_md(current_from_path: Path, current_dest_path: Path) -> tuple[Path, list[str]] | None:
    dir_items = [Path(i) for i in os.listdir(current_from_path)]
#     from_items: list[Path] = []
#     dest_items: list[Path] = []
#
#     for i in os.listdir(current_from_path):
#         from_items.append(Path(current_from_path / i))
#         dest_items.append(Path(current_dest_path / i))

    for item in dir_items:
        if Path(current_from_path / item).is_file() and item.suffix == '.md':
            # Generate html on correct directory
            generate_page(current_from_path / item, current_dest_path / item.with_suffix('.html'))
        elif Path(current_from_path / item).is_dir():
            # Call function in deeper founded dir
            crawl_for_md(current_from_path / item, current_dest_path / item)

def generate_page(from_path: Path, dest_path: Path, template_path = template_path):
    print(f"Generating page from {from_path} into {dest_path} using {template_path}")
    with open(from_path, encoding="utf-8") as file:
        md_file = file.read()

    with open(template_path, encoding="utf-8") as file:
        template_file = file.read()

    # Converting to html
    page_html = markdown_to_html_node(md_file).to_html()

    # Extract title
    page_title = extract_title(md_file)

    # Replace title place holder from the template
    splited_page = re.split(r"{{ Title }}", template_file)
    splited_page.insert(1, page_title)
    new_page = "".join(splited_page)

    # Replace content place holder from the template
    splited_page = []
    splited_page = re.split(r"{{ Content }}", new_page)
    splited_page.insert(1, page_html)
    new_page = "".join(splited_page)

    # Making sure the path exist
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, mode='w', encoding='utf-8') as file:
        file.write(new_page)


def main():
    generate_pages_recursive()

if __name__ == "__main__":
    main()
