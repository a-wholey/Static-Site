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