from textnode import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            result.append(old_node)
        else:
            text = old_node.text

            if text.count(delimiter) < 2:
                result.append(old_node)
            else:
                first_delim = text.find(delimiter)
                second_delim = text.find(delimiter, first_delim + len(delimiter))

                new_nodes = []
                
                before_text = text[:first_delim]
                if before_text:
                    new_nodes.append(TextNode(before_text, TextType.NORMAL))
                    
                between_text = text[first_delim + len(delimiter):second_delim]
                if between_text:
                    new_nodes.append(TextNode(between_text, text_type))
                    
                end_text = text[second_delim + len(delimiter):]
                if delimiter in end_text:
                    end_node = TextNode(end_text, TextType.NORMAL)
                    result.extend(new_nodes)
                    result.extend(split_nodes_delimiter([end_node], delimiter, text_type))
                else:
                    if end_text:
                        new_nodes.append(TextNode(end_text, TextType.NORMAL))
                    result.extend(new_nodes)

    return result

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            result.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)

        if len(images) == 0:
            result.append(old_node)
            continue

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.NORMAL))
            result.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.NORMAL))

    return result

def split_nodes_link(old_nodes):
    result = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            result.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            result.append(old_node)
            continue
            
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                result.append(TextNode(sections[0], TextType.NORMAL))
            result.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]

        if original_text != "":
            result.append(TextNode(original_text, TextType.NORMAL))

    return result