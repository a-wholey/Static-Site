from textnode import TextNode, TextType

def main():
    text = "this sucks"
    text_type = TextType.BOLD
    url = "https://boot.dev"
    node = TextNode(text, text_type, url)
    print(node)

if __name__ == "__main__":
    main()