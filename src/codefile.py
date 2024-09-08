from htmlnode import HTMLNode
from textnode import TextNode
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
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

            
            
            
                                   