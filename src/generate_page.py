from markdown_blocks import markdown_to_blocks, markdown_to_html_node
from htmlnode import ParentNode, LeafNode
from copystatic import copy_files_recursive
import os
import shutil

def extract_title(markdown):
    blocks = markdown.split("\n")
    if blocks[0].startswith("# "):
        return blocks[0].lstrip("# ").strip()
    raise Exception("No Title Found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    if not os.path.exists(from_path):
        raise Exception("Path not found")
    
    with open(from_path, encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, encoding="utf-8") as file_temp:
        template = file_temp.read()

    title = extract_title(markdown)
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    directory = os.path.dirname(dest_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir = os.listdir(dir_path_content)
    for item in dir:
        path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(path):
            dest_dir = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            dest_path = dest_path.replace(".md", ".html")
            generate_page(path, template_path, dest_path)
        else:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(path, template_path, dest_path)
            