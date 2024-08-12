import os
import shutil

from markdown_blocks import markdown_to_html_node


def copy_contents(source: str, destination: str):
    """Copy contents from static to public"""

    if not os.path.exists(source):
        raise ValueError(f'Directory {source} does not exist')

    # We delete the public directory to ensure new clean copy
    if os.path.exists(destination):
        shutil.rmtree(destination)

    # We recreate the directory
    os.mkdir(destination)

    # Iterate through items and copy
    for item in os.listdir(source):
        source_item = os.path.join(source, item)
        destination_item = os.path.join(destination, item)

        if os.path.isfile(source_item):
            shutil.copy(source_item, destination_item)
        else:
            copy_contents(source_item, destination_item)


def extract_title(markdown: str) -> str:
    markdown_lines = markdown.splitlines()
    for line in markdown_lines:
        if line.startswith('# '):
            return line[2:]

    raise ValueError('Could not find a valid title in the markdown')


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    # Read the from_path and template
    with open(from_path, 'r') as f, open(template_path, 'r') as t:
        markdown = f.read()
        template = t.read()

    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()

    title = extract_title(markdown)

    page = template.replace('{{ Title }}', title)
    page = page.replace('{{ Content }}', html_string)

    # Check if path exists before saving file
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Save page
    with open(dest_path, 'w') as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        source_item = os.path.join(dir_path_content, item)
        destination_item = os.path.join(dest_dir_path, item).replace('.md', '.html')

        if os.path.isfile(source_item):
            generate_page(source_item, template_path, destination_item)
        else:
            generate_pages_recursive(source_item, template_path, destination_item)
