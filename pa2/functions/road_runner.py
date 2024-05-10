from bs4 import BeautifulSoup

# TODO: preskoči tag script, style, meta, link, head

allowed_tags = ['div', 'h1', 'h2', 'p', 'title', 'table', 'html', 'body', 'tbody', 'tr', 'td']

class Node:
    def __init__(self, tag, text, classes, children, optional):
        self.tag = tag
        self.text = text
        self.classes = classes
        self.children = children
        self.optional = optional
        self.repeatable = False


def road_runner(pages):
    trees = []
    for page in pages:
        soup = BeautifulSoup(page, 'lxml')
        tree = build_dom_tree(soup.find("html"))

        trees.append(tree)

    wrapper = build_generalized_tree(trees[0], trees[1])
    print_dom_tree(None, wrapper)


def build_dom_tree(tag):
    node = Node(tag.name, tag.string if tag.string else None, tag.attrs.get('class', []), [], False)

    if allowed_tags is None or tag.name in allowed_tags:
        for child in tag.children:
            if isinstance(child, str):
                continue

            if child.name in allowed_tags:
                node.children.append(build_dom_tree(child))

    return node

def build_generalized_tree(tree1, tree2):
    if tree1.tag != tree2.tag:
        tree1.optional = True
        return tree1

    if check_string_mismatch(tree1, tree2):
        tree1.text = "#PCDATA"

    else:
        if tree1.children:
            for index in range(min(len(tree1.children), len(tree2.children))):
                tree1.children[index] = build_generalized_tree(tree1.children[index], tree2.children[index])

            if len(tree1.children) > len(tree2.children):
                for index in range(len(tree2.children), len(tree1.children)):
                    tree1.children[index].optional = True
            else:
                for index in range(len(tree1.children), len(tree2.children)):
                    tree2.children[index].optional = True
                    tree1.children.append(tree2.children[index])
        elif tree2.children:
            # Set children as optional
            tree1.children = [child for child in tree2.children]
            for child in tree1.children:
                child.optional = True

        else:
            return tree1

    return tree1

def check_repeated_nodes(node1, node2):
    if node1 is None or node2 is None:
        return False

    if node1.tag != node2.tag:
        return False

    if not node1.children and not node2.children:
        return True

    if node1.children and not node2.children or not node1.children and node2.children:
        return False

    if node1.classes != node2.classes:
        return False

    for index in range(len(node1.children)):
        repeatable = False if index >= len(node2.children) else check_repeated_nodes(
            node1.children[index], node2.children[index])
        if not repeatable:
            return False

    return True

def check_string_mismatch(node1, node2):
    if node1.text and node2.text:
        return node1.text != node2.text
    return False

def print_dom_tree(prev_node, node, depth=0):
    if node:
        repeated_string_opening = ""
        repeated_string_closing = ""

        if prev_node and check_repeated_nodes(prev_node, node):
            repeated_string_opening = "("
            repeated_string_closing = ")+"

        # classes_str = ' '.join(node.classes)
        opening_tag = "<" + node.tag
        # if classes_str:
        #     opening_tag += ' class="' + classes_str + '"'
        opening_tag += ">"
        print(repeated_string_opening + opening_tag, end="")
        if node.text:
            print(node.text, end="")
        for child in node.children:
            if isinstance(child, str):
                print(child, end="")
            else:
                print_dom_tree(node, child, depth + 1)
        print(f"</{node.tag}>" + repeated_string_closing, end="")
