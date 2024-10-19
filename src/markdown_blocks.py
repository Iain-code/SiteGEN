from textnode import text_node_to_html_node
from htmlnode import ParentNode
from codefile import text_to_text_nodes
import os
from pathlib import Path

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    items = []
    for item in split:
        item = item.strip()
        items.append(item)
    return items

def block_to_block_type(markdown_text):
    split = markdown_text.split("\n")
    
    for line in split:
        if line.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return "Heading"
    if all(line.startswith(">") for line in split):
        return "quote"
    if all(line.startswith(("* ", "- ")) for line in split):
        return "unordered list"
            
    if markdown_text.startswith("1. "):
        i = 1
        for line in split:
            if line.startswith(f"{i}. "):
                return "ordered list"
            i += 1
        return "paragraph"

    if split[0] == "```" and split[-1] == "```":
        return "code"
    if markdown_text.startswith("```") and markdown_text.endswith("```"):
        return "code"
    
    return "paragraph"

def markdown_to_html_node(markdown):

    parent_node = ParentNode("div", children=[]) # children will be a list of the HTMLNodes
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "quote":
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.strip(">").strip()) # Strips ">" and all whitespace at start and end of line.
            content = " ".join(new_lines)               # re joins the elements together with a " " between them
            nodes = text_to_text_nodes(content)  # this gives a LIST of TextNodes when given the string content
            children = []
            for node in nodes:   # we need to split the list into nodes to give them to text_node_to_html_node()
                html_node = text_node_to_html_node(node)
                children.append(html_node)
            blockquote_node = ParentNode(tag="blockquote", children=children)
            parent_node.children.append(blockquote_node)
                  
        if block_type == "Heading":
            level = 0
            for char in block:
                if char == "#":
                    level += 1
                else: 
                    break                 

            strip = block[level:].strip()
            content = "".join(strip)
               
            nodes = text_to_text_nodes(content)
            children = []
            for node in nodes:
                html_node = text_node_to_html_node(node)
                children.append(html_node)
            heading_node = ParentNode(tag=f"h{level}", children=children)
            parent_node.children.append(heading_node)

        
        if block_type == "code":
            
            content = block[3:-3].strip()
            nodes = text_to_text_nodes(content)
            children = []
            for node in nodes:
                html_node = text_node_to_html_node(node)
                children.append(html_node)
            code_node = ParentNode(tag="code", children=children)
            pre_node = ParentNode(tag="pre", children=[code_node])
            parent_node.children.append(pre_node)
           
        if block_type == "unordered list":
            lines = block.split("\n")   # Text string comes in and is split into list of elements at the line break
            li_nodes = [] 
            for line in lines:
                if line.startswith("* ") or line.startswith("- "): # for each line check if it starts with * or -
                    content = line[2:].strip()      # strip away unwanted characters and start text and first normal char
                    nodes = text_to_text_nodes(content) # gives back a list of TextNodes from the string(content)
    
                    children = []
                    for node in nodes:
                        html_node = text_node_to_html_node(node)
                        children.append(html_node)  # append each HTMLNode to children (list)
            
                    li_node = ParentNode(tag="li", children=children)# make the list of children, children parameter in this Node
                    li_nodes.append(li_node) # add the li_node to the list of li_nodes
                else:
                    raise Exception("Not a uList")
                    
            ulist_node = ParentNode(tag="ul", children=li_nodes)
            parent_node.children.append(ulist_node)
       
        if block_type == "ordered list":
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                content = line[2:].strip() # stips the 1. or 2. etc...
                nodes = text_to_text_nodes(content)

                children = []
                for node in nodes:  # we need this second for loop incase there are inline markdowns like bold or italic
                    html_node = text_node_to_html_node(node)
                    children.append(html_node)
                
                li_node = ParentNode(tag="li", children=children)
                li_nodes.append(li_node)

            olist_node = ParentNode(tag="ol", children=li_nodes)
            parent_node.children.append(olist_node)
      
        if block_type == "paragraph":
            nodes = []
            lines = block.split("\n")
            paragraph = " ".join(lines)

            text_nodes = text_to_text_nodes(paragraph)
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                nodes.append(html_node)

            paragraph_node = ParentNode(tag="p", children=nodes)
            parent_node.children.append(paragraph_node)

    return parent_node



def extract_title(markdown):
    lines = markdown.split("\n")

    for line in lines:
        line = line.strip()
        if line == "":
            continue
        if line.startswith("#"):
            heading = line.strip("# ")
            return heading
        else: 
            raise Exception("No heading found")

def generate_page(from_path, template_path, dest_path):

    print(f"gen_page from path: {from_path}")
    print(f"gen_page template path: {template_path}")
    print(f"gen_page destination path: {dest_path}")

    print(f"Generating page FROM PATH: {from_path}\nDESTINATION PATH: {dest_path}\nTEMPLATE PATH: {template_path}")
    
    with open(from_path, 'r') as file:
        content_f = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    
    print("read files")

    new_content = markdown_to_html_node(content_f)
    print("content_f through markdown to html node")

    content = new_content.to_html()
    title = extract_title(content_f)

    replaced = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
    print("title and content replaced")

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    print("new destination path created")

    with open(dest_path, 'w') as file:
        file.write(replaced)
    print("file written to dest_path")
    print(f"FINISHED GENERATING PAGE")


def generate_pages_recursive(content_path, template_path, public_path):

    public_path = Path(public_path)
    here = os.getcwd()
    template_path = os.path.join(here, "./template.html")

    if not os.path.exists(content_path):
        print(f"Directory does not exist: {content_path}")
        return
    
    items = os.listdir(content_path) # make a list of every file/dir in content
    
    if items:
        for item in items:
            item_path = Path(content_path) / item

            source = Path(content_path)
            print(f"source: {source}")
            destination = Path(public_path)
            print(f"destination: {destination}")

            if os.path.isdir(item_path):
            
                print("Directory found")
                print(f"item path = {item_path}")
            
                new_content_path = source / item_path.name
                print(f"NEW CONTENT PATH: {new_content_path}")
                new_dest_path = destination / new_content_path.name
                print(f"new dest path: {new_dest_path}")
                os.mkdir(new_dest_path) # make a new DIRECTORY in the destination
                
                generate_pages_recursive(new_content_path, template_path, new_dest_path) # call the function again on the NESTED dir
                
            else: 
        
                if os.path.exists(content_path) and item.endswith(".md"):
                    print(".md file found")
                    print(f"item path: {item_path}")
                    print(f"PUBLIC PATH = {public_path}")
                    # Define the path to the directory and the new file

                    new_file_path = public_path / "index.html"
                    print(f"new file path: {new_file_path}")
                    # To create an empty file, or ensure a file exists
                    new_file_path.touch()
                    generate_page(item_path, template_path, new_file_path)
                
                