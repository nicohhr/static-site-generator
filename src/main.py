from textnode import TextNode, TextType

def main():

    test_node = TextNode("Lorem Ipsum", TextType.PLAIN_TEXT, "www.github.com")
    print(test_node)

main()
