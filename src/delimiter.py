from textnode import TextNode
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"
    new_node_list = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            count = node.text.count(delimiter)
            if count % 2 != 0:
                raise Exception("Expecting markdown pair")
            
            is_text_type = node.text.startswith(delimiter)
            is_text_type2 = node.text.endswith(delimiter)
            parts = node.text.split(delimiter)
            if is_text_type:
                parts.pop(0)
            if is_text_type2:
                parts.pop()

            for i, part in enumerate(parts):
                 if (i % 2 == 0 and not is_text_type) or (i % 2 != 0 and is_text_type):
                    # Text parts
                    new_node_list.append(TextNode(part, "text"))
                 else:
                    # Formatted text parts
                    new_node_list.append(TextNode(part, text_type))
        else:
            new_node_list.append(node)
            
    return new_node_list
def extract_markdown_images(text):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_list.append(node)
        else:
            node_text = node.text
            for i in range(0, len(images)):
                if len(node_text) == 0:
                    break
                temp_split = node_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
                if len(temp_split[0]) != 0:
                    new_list.append(TextNode(temp_split[0], "text"))
                new_list.append(TextNode(images[i][0], "image", images[i][1]))
                if len(temp_split[1]) == 0:
                    break
                if i == len(images) - 1:
                    new_list.append(TextNode(temp_split[1], "text"))
                    break
                node_text = temp_split[1]
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_list.append(node)
        else:
            node_text = node.text
            for i in range(0, len(links)):
                if len(node_text) == 0:
                    break
                temp_split = node_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
                if len(temp_split[0]) != 0:
                    new_list.append(TextNode(temp_split[0], "text"))
                new_list.append(TextNode(links[i][0], "link", links[i][1]))
                if len(temp_split[1]) == 0:
                    break
                if i == len(links) - 1:
                    new_list.append(TextNode(temp_split[1], "text"))
                    break
                node_text = temp_split[1]
    return new_list

def text_to_textnodes(text):
    nodes = [TextNode(text, "text")]
    nodes = split_nodes_delimiter(nodes, "**", "bold")
    nodes = split_nodes_delimiter(nodes, "*", "italic")
    nodes = split_nodes_delimiter(nodes, "`", "code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

