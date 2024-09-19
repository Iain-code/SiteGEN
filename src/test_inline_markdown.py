import unittest
from codefile import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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
        node = TextNode("This is text with some `code` words", text_type_code)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
    
    
    def test_regex_image(self):
        node = "This is some text with an ![this is a picture of a dog](dog picture) in it"
        new_node = extract_markdown_images(node)
        self.assertListEqual([("this is a picture of a dog", "dog picture")], new_node)
    
    def test_regex_link(self):
        node = "This is some text with a [Duck Duck Go](https://duckduckgo.com) in it"
        new_node = extract_markdown_links(node)
        self.assertEqual([("Duck Duck Go", "https://duckduckgo.com")], new_node)


if __name__ == "__main__":
    unittest.main()
