import re
from htmlnode import HTMLNode
from textnode import TextNode
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
            raise Exception("Delimiter has no close marker")
        
        for index, section in enumerate(sections): # we must use enumerate to get an index number for the list "index" so that we can
                                            # use the % function to check if we need to use the text_type or text_type_text.
            if section == "":               # otherwise we could use for i in range len(sections) - this gives us an index num also
                continue
             
            if index % 2 == 0:
                split_nodes.append(TextNode(section, text_type_text))
            else:
                index % 2 !=0
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
    pattern = r"(!\[.*?\]\(.*?\))"
    pattern_alt = r"!\[.*?\]"
    pattern_image = r"\(.*?\)"
    for node in old_nodes:
        sections = re.split(pattern, node.text)
        for section in sections:
            if section != pattern:
                new_node = node.text + text_type_text
                new_nodes.append(new_node)
            else:
                split_sec = section.split(f"![{pattern_alt}]({pattern_image})", 1)
                new_section = split_sec[0] + text_type_image
                new_nodes.append(new_section, pattern_image)
    return new_nodes
        

def split_nodes_link(old_nodes):

    pattern = r"(\[.*?\]\(.*?\))"                      