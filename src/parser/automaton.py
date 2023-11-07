from parser.data.tree import RootNode, EndNode, InterimNode, Node
from parser.utils.text import normalize_word


class Automaton:
    root: RootNode

    def __init__(self) -> None:
        self.root = RootNode()

    def validate_input(self, s: str) -> None:
        ...

    def validate_dictionary(self, s: str) -> None:
        ...

    def scan(self, _input: str) -> int:
        return 0

    def add_word(self, word: str) -> None:
        normalized_word = normalize_word(word)
        depth = len(normalized_word)

        current_node: Node = self.root
        for index, char in enumerate(normalized_word):
            is_last_node = index == depth - 1

            if char in current_node.children:
                max_depth = max(current_node.children[char].depth, depth)

                if is_last_node:
                    match current_node.children[char]:
                        case EndNode() as end_node:
                            current_node.children[char] = EndNode(
                                children=end_node.children,
                                value=char,
                                depth=max_depth,
                                factor=end_node.factor + 1,
                            )
                        case InterimNode() as im:
                            current_node.children[char] = EndNode(
                                children=im.children,
                                value=char,
                                depth=max_depth,
                                factor=1,
                            )

                match current_node:
                    case RootNode():
                        ...
                    case _:
                        current_node.depth = max_depth

                current_node = current_node.children[char]
                current_node.depth = max_depth
            else:
                match current_node:
                    case RootNode():
                        max_depth = depth
                    case node:
                        max_depth = max(node.depth, depth)

                new_node: InterimNode | EndNode = EndNode(value=char, depth=max_depth, factor=1) \
                    if is_last_node \
                       else InterimNode(value=char, depth=max_depth)

                current_node.children[char] = new_node
                current_node = new_node
