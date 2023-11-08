import copy

from typing import List

from parser.data.mutable_state import MutableState
from parser.data.trie import RootNode, EndNode, InterimNode, Node
from parser.utils.text import normalize_word


class Automaton:
    def __init__(self) -> None:
        self.root: RootNode = RootNode()

    def validate_input(self, s: str) -> None:
        ...

    def validate_dictionary(self, s: str) -> None:
        ...

    def scan(self, text: str) -> int:
        print(f'Scan: "{text}"')

        result = 0

        current_states: List[MutableState] = []
        next_states: List[MutableState] = []

        for char in text:
            while current_states:
                print(current_states)

                current_state = current_states.pop()

                match current_state.node[char]:
                    case EndNode(factor=factor) as end_node:  # Word found!
                        result += factor
                        print(f'+{factor} ET: {current_state.node.value} -> {end_node.value} (carry: {list(current_state.carry_queue)})')
                        print(self.root.prettify())
                        end_node.factor = 0  # TODO Update node type / write it to (seen) / remove all factor 0

                        next_state = MutableState(
                            node=end_node,
                            carry_queue=copy.copy(current_state.carry_queue),
                            carry_index=copy.copy(current_state.carry_index),
                        )

                        next_states.append(next_state)
                    case InterimNode() as im_node:  # Go without additional carry
                        print(f'IT: {current_state.node.value} -> {im_node.value} (carry: {list(current_state.carry_queue)})')

                        next_state = MutableState(
                            node=im_node,
                            carry_queue=copy.copy(current_state.carry_queue),
                            carry_index=copy.copy(current_state.carry_index),
                        )

                        next_states.append(next_state)

                # carry_queue = list(current_state.node.children.values())
                # while carry_queue:
                #     carry_child = carry_queue.pop()

                #     if carry_child.value in current_state.carry_index:

                #         next_state = MutableState(
                #             node=carry_child,
                #             carry_queue=copy.copy(current_state.carry_queue),
                #             carry_index=copy.copy(current_state.carry_index),
                #         )

                #         next_state.remove(carry_child.value)
                #         print(next_state)
                #         next_states.append(next_state)

                current_state.carry(char)
                next_states.append(current_state)

            match self.root[char]:
                case InterimNode() | EndNode() as node:
                    state = MutableState(node)
                    next_states.append(state)
                    print(f'ST: * -> {state.node.value}')

            current_states, next_states = next_states, []

        print(current_states)
        print(result)
        return result

    def add_word(self, word: str) -> None:
        normalized_word = normalize_word(word)
        depth = len(normalized_word)

        current_node: Node = self.root
        for carry_index, char in enumerate(normalized_word):
            is_last_node = carry_index == depth - 1

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
