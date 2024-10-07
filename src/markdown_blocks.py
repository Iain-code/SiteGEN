from textnode import text_node_to_html_node
from htmlnode import ParentNode
from codefile import text_to_text_nodes

def markdown_to_blocks(markdown):
    split = markdown.split("\n\n")
    items = []
    for item in split:
        if item == "":
            continue
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
    if all(line.startswith(("*", "-")) for line in split):
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
                if line.startswith("*") or line.startswith("-"): # for each line check if it starts with * or -
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
            joined = " ".join(lines)

            text_nodes = text_to_text_nodes(joined)
            for node in text_nodes:
                html_node = text_node_to_html_node(node)
                nodes.append(html_node)

            paragraph_node = ParentNode(tag="p", children=nodes)
            parent_node.children.append(paragraph_node)

    return parent_node