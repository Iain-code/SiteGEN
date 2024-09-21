import unittest
from codefile import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)
class TestInlineMarkdown(unittest.TestCase):
    def test_nodes_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        self.assertListEqual([
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text)], new_nodes)
    
    def test_nodes_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        
        self.assertListEqual([
            TextNode("This is text with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text)], new_nodes)
        
    def test_nodes_code(self):
        node = TextNode("This is text with some `code` words", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual([
            TextNode("This is text with some ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" words", text_type_text)], new_nodes)

    
    def test_regex_image(self):
        node = "This is some text with an ![this is a picture of a dog](the picture) in it"
        new_node = extract_markdown_images(node)
        self.assertListEqual([("this is a picture of a dog", "the picture")], new_node)
    
    def test_regex_link(self):
        node = "This is some text with a [Duck Duck Go](https://duckduckgo.com) in it"
        new_node = extract_markdown_links(node)
        self.assertListEqual([("Duck Duck Go", "https://duckduckgo.com")], new_node)


    def test_split_nodes_image(self):
        node = TextNode("This is some text with a ![alt image](image here)", text_type_text)
        new_node = split_nodes_image([node])             
        self.assertListEqual([
            TextNode("This is some text with a ", text_type_text),
            TextNode("alt image", text_type_image, "image here")], new_node) 
            # we are making sure all that written Text Nodes are the same as new_node

    def test_split_nodes_image_full(self):
        node = TextNode("This is some text with a ![alt image](image here) and text after", text_type_text)
        new_node = split_nodes_image([node]) # this is a list because the full function will expect a list
        self.assertListEqual([
            TextNode("This is some text with a ", text_type_text),
            TextNode("alt image", text_type_image, "image here"),
            TextNode(" and text after", text_type_text)], new_node)
        
    def test_split_nodes_link(self):
        node = TextNode("This is some text with a [link](www.link.com)", text_type_text)
        new_node = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is some text with a ", text_type_text),
            TextNode("link", text_type_link, "www.link.com")], new_node)
        
    def test_split_nodes_link_full(self):
        node = TextNode("This is some text with a [link](www.link.com) and text after", text_type_text)
        new_node = split_nodes_link([node])
        self.assertListEqual([
            TextNode("This is some text with a ", text_type_text),
            TextNode("link", text_type_link, "www.link.com"),
            TextNode(" and text after", text_type_text)], new_node)        

if __name__ == "__main__":
    unittest.main()
