import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
    )

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
    
        if len(sections) % 2 == 0:
            raise ValueError("Markdown is wrong")
        
        for index, section in enumerate(sections): # we must use enumerate to get an index number for the list "index" so that we can
                                            # use the % function to check if we need to use the text_type or text_type_text.
            if section == "":               # otherwise we could use for i in range len(sections) - this gives us an index num also
                continue
             
            if index % 2 == 0:
                split_nodes.append(TextNode(section, text_type_text))
            if index % 2 != 0:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches
    
def extract_markdown_links(text):
    pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

            
def split_nodes_image(old_nodes):

    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:  # Making sure the node is not already text_type_text
            new_nodes.append(old_node)
            continue

        new_text = old_node.text
        images = extract_markdown_images(new_text) # provides a list of tuples with alt-text and URLs in.    
        

        if len(images) == 0:
            new_nodes.append(old_node) # make sure that nodes with no markdown are not put through the function
            continue

        for image in images:
            sections = new_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            for alt_text, url in images: # Matches is a list of "2 item" tuples, first item is named alt_text, 2nd is url. Then to next tuple
                new_nodes.append(TextNode(alt_text, text_type_image, url))
            if sections[1] != "":
                new_nodes.append(TextNode(sections[1], text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        
        new_text = old_node.text
        links = extract_markdown_links(new_text)
        
        if len(links) == 0:
            new_nodes.append(old_node) # make sure that nodes with no markdown are not put through the function
            continue
    
        for link in links:
            sections = new_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            for text, url in links:
                new_nodes.append(TextNode(text, text_type_link, url))
            if sections[1] != "":
                new_nodes.append(TextNode(sections[1], text_type_text))
    return new_nodes

def text_to_text_nodes(text):
    nodes = [TextNode(text, text_type_text)]   # This is the output, will give a list of all of the respective nodes
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
        
   

