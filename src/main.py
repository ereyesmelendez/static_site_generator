import os
import shutil
from textnode import TextNode
from markdown_blocks import generate_page

def copy_directory(src, dest):
    if not os.path.exists(src):
        print("This source directory {src} does not exist.")
        return
    
    if os.path.exists(dest):
        shutil.rmtree(dest)

    os.makedirs(dest)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            copy_directory(src_item, dest_item)

        else: 
            shutil.copy(src_item, dest_item)
            print(f"Copied file {src_item} to {dest_item}")
        


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)
    print("Starting copy operation...")
    src_directory = 'static'
    dest_directory = 'public'
    copy_directory(src_directory, dest_directory)
    print("Copy operation completed.")

    print("Current working directory:", os.getcwd())
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    public_directory = os.path.join(base_dir, 'public')
    static_directory = os.path.join(base_dir, 'static')
    from_path = os.path.join(base_dir, 'content', 'index.md')
    template_path = os.path.join(base_dir, 'template.html')
    dest_path = os.path.join(public_directory, 'index.html')
    
    # Print paths for debugging
    print(f"Base directory: {base_dir}")
    print(f"Public directory: {public_directory}")
    print(f"Static directory: {static_directory}")
    print(f"Markdown path: {from_path}")
    print(f"Template path: {template_path}")
    print(f"Destination path: {dest_path}")

    if os.path.exists(public_directory):
        shutil.rmtree(public_directory)

    if os.path.exists(static_directory):
        shutil.copytree(static_directory, public_directory)

    generate_page(from_path, template_path, dest_path)

    
if __name__ == "__main__":
    main()