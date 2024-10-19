from textnode import TextNode
import shutil
import pathlib
import os
from markdown_blocks import generate_page, generate_pages_recursive

source = "/home/iain/workspace/github.com/NewProjects/SiteGEN/static"
destination = "/home/iain/workspace/github.com/NewProjects/SiteGEN/public"
   
def main():
    pass
    
def cleaning_directory(destination):

    now = os.getcwd()               # this is finding the current working directory (CWD)
    source = os.path.join(now, "static")        # This is making source directory by joining now and static folder.
    destination = os.path.join(now, "public")   # same as static


    for item in os.listdir(destination):    # makes a list of the public folder files / dir
        if not os.listdir(destination):
            raise Exception("No directory")

        item_path = os.path.join(destination, item)  # gives new path name for each file
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)   # if "item" is a directory we remove the whole thing
          
        else:
            os.remove(item_path)   # if "item" is a file then we just remove that file
    print("DIRECTORY CLEANED")
 
        
def copying(source, destination):  # copies the files and dir from static into public
    
    check_s = os.path.exists(source)

    check_d = os.path.exists(destination)


    if not check_d:
        os.makedirs(destination)
    

    list_dir = os.listdir(source)       # making a list from the files in source

    for item in list_dir:
        new_path = os.path.join(source, item) # give full pathname for item adding source and item together
        if os.path.isfile(new_path):
            shutil.copy(new_path, destination)  # if its a file then we copy it over to destination
      
        else:
            os.path.isdir(new_path)      
            new_destination = os.path.join(destination, item) # make a new DIRECTORY in the destination

            copying(new_path, new_destination)   # if its not then we call function again to make another list
    print("COPYING COMPELTE")

    
here = os.getcwd()
content_path = os.path.join(here, "content")
template_path = os.path.join(here, "template.html")
public_path = os.path.join(here, "public")

if __name__ == "__main__":
    print("=== Script started ===")
    cleaning_directory(destination)
    copying(source, destination)
    generate_pages_recursive(content_path, template_path, public_path)
    print("=== Script ended ===")