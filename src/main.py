from textnode import TextNode
import shutil
import pathlib
import os


   
def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(node)

now = os.getcwd()               # this is finding the current working directory (CWD)
source = os.path.join(now, "./static")        # This is making source directory by joining now and static folder.
destination = os.path.join(now, "./public")   # same as static

print(f"source: {source}")
print(f"destination: {destination}")

def cleaning_directory(destination):
    for item in os.listdir(destination):    # makes a list of the public folder files / dir
        if not os.listdir(destination):
            print("No directory or files")

        item_path = os.path.join(destination, item)  # gives new path name for each file
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)   # if "item" is a directory we remove the whole thing
        else:
            os.remove(item_path)   # if "item" is a file then we just remove that file
        
def copying(source, destination):
    
    check_s = os.path.exists(source)
    print(check_s)
    check_d = os.path.exists(destination)
    print(check_d)

    list_dir = os.listdir(source)       # making a list from the files in source
    for item in list_dir:
        check = os.path.isfile(item)    # making sure that "item" is a file not a directory
        print(check)
        if check == True:              
            shutil.copy(item, destination)  # if its a file then we copy it over to destination 
        if check == False:
            copying(source, destination)   # if its not then we call function again to make another list
        if not os.path.isdir and not os.path.isfile(source):
            break
        
        

if __name__ == "__main__":
    cleaning_directory(destination)
    copying(source, destination)


main()