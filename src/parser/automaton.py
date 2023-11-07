from parser.data.tree import RootNode, EndNode, IntermediateNode, Node
from parser.utils.text import normalize_word


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
                max_depth = max(current_node.children[char].depth, depth)

                if is_last_node:
                    match current_node.children[char]:
                        case IntermediateNode() as im:
                            current_node.children[char] = EndNode(char, max_depth)
                            current_node.children[char].children = im.children

                match current_node:
                    case IntermediateNode() as im:
                        current_node.depth = max_depth

                current_node = current_node.children[char]
                current_node.depth = max_depth
            else:
                match current_node:
                    case IntermediateNode() as im:
                        max_depth = max(im.depth, depth)
                    case _:
                        max_depth = depth

                new_node: IntermediateNode = EndNode(char, max_depth) if is_last_node else IntermediateNode(char, max_depth)
                current_node.children[char] = new_node
                current_node = new_node
