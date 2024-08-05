import os
import shutil
from textnode import TextNode

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

    
if __name__ == "__main__":
    main()