from textnode import TextNode
import shutil
import pathlib
import os
from markdown_blocks import generate_page


   
def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    
def cleaning_directory(destination):

    now = os.getcwd()               # this is finding the current working directory (CWD)
    source = os.path.join(now, "./static")        # This is making source directory by joining now and static folder.
    destination = os.path.join(now, "./public")   # same as static

    print(f"source: {source}")
    print(f"destination: {destination}")

    for item in os.listdir(destination):    # makes a list of the public folder files / dir
        if not os.listdir(destination):
            print("No directory or files")

        item_path = os.path.join(destination, item)  # gives new path name for each file
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)   # if "item" is a directory we remove the whole thing
            print("Remove dir")
        else:
            os.remove(item_path)   # if "item" is a file then we just remove that file
            print("remove item")
        
def copying(source, destination):
    
    check_s = os.path.exists(source)
    print(check_s)
    check_d = os.path.exists(destination)
    print(check_d)

    if not check_d:
        os.makedirs(destination)
        print("make new destination")

    list_dir = os.listdir(source)       # making a list from the files in source

    for item in list_dir:
        new_path = os.path.join(source, item) # give full pathname for item adding source and item together
        if os.path.isfile(new_path):
            shutil.copy(new_path, destination)  # if its a file then we copy it over to destination
            print("File copied") 
        else:
            os.path.isdir(new_path)      
            new_destination = os.path.join(destination, item) # make a new DIRECTORY in the destination
            print("new dir made")
            copying(new_path, new_destination)   # if its not then we call function again to make another list

    
if __name__ == "__main__":
    main()