from src.data.tree import RootNode, EndNode, IntermediateNode, Node
from src.utils.text import normalize_word


class Automaton:
    root: RootNode

    def __init__(self) -> None:
        self.root = RootNode()

    def add_word(self, word: str) -> None:
        normalized_word = normalize_word(word)  # compaction

        current_node: Node = self.root
        depth = len(normalized_word)

        for index, char in enumerate(normalized_word):
            is_last_node = index == depth - 1

            if char in current_node.children:

                match current_node:
                    case IntermediateNode():
                        current_node.depth = max(current_node.depth, depth)

                if is_last_node:
                    match current_node.children[char]:
                        case IntermediateNode() as im:
                            current_node.children[char] = EndNode(char, max(im.depth, depth))
                            current_node.children[char].children = im.children

                current_node = current_node.children[char]
            else:
                new_node: Node = EndNode(char, depth) if is_last_node else IntermediateNode(char, depth)
                current_node.children[char] = new_node
                current_node = new_node
