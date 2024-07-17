from htmlnode import ParentNode, HTMLNode, LeafNode
from textnode import TextNode, text_node_to_html_node
from delimiter import text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    mega_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        text = trim_block(block, block_type)
        if block_type == "ordered_list":
            lines = text.split("\n")
            order_children = []
            for line in lines:
                order_children.append(ParentNode("li", text_to_children(line)))
            mega_children.append(ParentNode("ol", order_children))

        if block_type == "code":
            text = text.replace("\n", " ")
            contents = ParentNode("code", text_to_children(text))
            mega_children.append(ParentNode("pre", [contents]))

        if block_type == "heading":
            split = block.split(" ", 1)
            count = split[0].count("#")
            mega_children.append(ParentNode(f"h{count}", text_to_children(text)))

        if block_type == "quote":
            text = text.replace("\n", " ")
            mega_children.append(ParentNode("blockquote", text_to_children(text)))

        if block_type == "unordered_list":
            lines = text.split("\n")
            order_children = []
            for line in lines:
                order_children.append(ParentNode("li", text_to_children(line)))
            mega_children.append(ParentNode("ul", order_children))

        if block_type == "paragraph":
            text = text.replace("\n", " ")
            mega_children.append(ParentNode("p", text_to_children(text)))

    print(mega_children)
    return ParentNode("div", mega_children)

        

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

def trim_block(block, block_type):
    lines = block.split("\n")

    if block_type == "code":
       return "\n".join(lines[1:-1])
    
    if block_type == "heading":
        return block.lstrip("# ")

    if block_type == "ordered_list":
        new_list =[]
        for line in lines:
            parts = line.split(" ", 1)
            if len(parts) > 1:
                new_list.append(parts[1])
        return "\n".join(new_list)
    
    if block_type == "paragraph":
        return "\n".join(lines)
    
    if block_type == "quote":
        new_list =[]
        for line in lines:
            parts = line.split(" ", 1)
            if len(parts) > 1:
                new_list.append(parts[1])
        return "\n".join(new_list)
    
    if block_type == "unordered_list":
        new_list =[]
        for line in lines:
            parts = line.split(" ", 1)
            if len(parts) > 1:
                new_list.append(parts[1])
        return "\n".join(new_list)
    
