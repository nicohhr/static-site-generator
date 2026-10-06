import re

from blocknode import *
from markdown_utils import *

from_path = "content/index.md"
dest_path = "public/index.html"
template_path = "template.html"

def generate_page():
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

    with open(dest_path, mode='+w', encoding='utf-8') as file:
        file.write(page_html)

    # print(page_html)

def main():
    generate_page()

if __name__ == "__main__":
    main()
