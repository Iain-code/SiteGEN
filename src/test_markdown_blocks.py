import unittest
from markdown_blocks import block_to_block_type, markdown_to_blocks, markdown_to_html_node, extract_title, generate_page

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        node = """
This is a **bold** word.

This has some *italic* and `code` words inside of it.
This is a new paragraph on a new line.

* This is a list
* With another item
"""
        new_node = markdown_to_blocks(node)
        self.assertEqual(
            [
            "This is a **bold** word.", 
            "This has some *italic* and `code` words inside of it.\nThis is a new paragraph on a new line.",
            "* This is a list\n* With another item",
            ], new_node)
    
    def test_markdown_to_block(self):
        node = """
This is a new **paragraph**.
I would like *this* to work `first` time. 

* It better
* Not fuck up
"""
        new_node = markdown_to_blocks(node)
        self.assertEqual([
            "This is a new **paragraph**.\nI would like *this* to work `first` time.",
            "* It better\n* Not fuck up",
        ], new_node)

    def test_block_to_block_type_heading(self):
        node = """
# Heading one
# Heading two
"""
        new_node = block_to_block_type(node)
        self.assertEqual("Heading", new_node)

    def test_block_to_block_type_quote(self):
        node = """>This is all a quote
>Its a quote because I just said it"""

        new_node = block_to_block_type(node)
        self.assertEqual("quote", new_node)

    def test_block_to_block_type_code(self):
        node = """```unordered list of things
Another thing
One more thing
Last thing```"""
        new_node = block_to_block_type(node)
        self.assertEqual("code", new_node)
    
    def test_block_to_block_type_olist(self):
        node = """1. Ordered list of thing
2. Another thing
3. Three things
4. Four things"""
        new_node = block_to_block_type(node)
        self.assertEqual("ordered list", new_node)  

    def test_markdown_to_html_node_headings(self):

        node = "# this is heading"
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><h1>this is heading</h1></div>")


    def test_blockquote(self):

        node = """
> This should be a quote
> So should this
> This aswell
"""
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><blockquote>This should be a quote So should this This aswell</blockquote></div>")


    def test_ordered_list(self):
        
        node = """
1. One
2. Two
3. Three
"""
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><ol><li>One</li><li>Two</li><li>Three</li></ol></div>")
    
    def test_unordered_list(self):

        node = """
* One
- Two
* Three
- Four
"""
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><ul><li>One</li><li>Two</li><li>Three</li><li>Four</li></ul></div>")

    def test_paragraph(self):

        node = "This is just a paragraph"
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><p>This is just a paragraph</p></div>")

    def test_code(self):

        node = "```This is some really great code I wrote```"
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        self.assertEqual(html, "<div><pre><code>This is some really great code I wrote</code></pre></div>")

    def test_mixed(self):

        node = """

# Heading

> This is going
> to be a little

1. To be
2. a little

* Hope
* Pray

```Some code```
"""
        new_node = markdown_to_html_node(node)
        html = new_node.to_html()
        text = """<div><h1>Heading</h1><blockquote>This is going to be a little</blockquote><ol><li>To be</li><li>a little</li></ol><ul><li>Hope</li><li>Pray</li></ul><pre><code>Some code</code></pre></div>"""
        self.assertEqual(html, text)

    def test_extract_title(self):

        node = "# Piggy wiggy"
        new_node = extract_title(node)
        self.assertEqual(new_node, "Piggy wiggy")

    def test_extract_title_again(self):

        node = """
# This better come out good

> or shit will hit
> the fan...
"""
        new_node = extract_title(node)
        self.assertEqual(new_node, "This better come out good")

if __name__ == '__main__':
    unittest.main()