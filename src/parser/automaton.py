import copy

from typing import List

from parser.data.mutable_state import MutableState
from parser.data.trie import Node
from parser.data.trie import RootNode
from parser.utils.text import normalize_word


class Automaton:
    def __init__(self) -> None:
        self.root: RootNode = RootNode()

    def add_word(self, word: str) -> None:
        normalized_word = normalize_word(word)
        word_depth = len(normalized_word)  # word depth determines a sliding window size

        current_node: Node = self.root
        for index, char in enumerate(normalized_word):
            is_term_char = index == word_depth - 1

            if char in current_node.children:  # char has already been visited
                child = current_node[char]
                max_depth = max(child.depth, word_depth)
                child.weight += 1
                child.terminator = child.terminator or is_term_char
                child.depth = max_depth
            else:
                max_depth = max(current_node.depth, word_depth)

                child = Node(parent=current_node,
                             value=char,
                             depth=max_depth,
                             terminator=is_term_char)

                current_node[char] = child

            current_node = child

    def scan(self, text: str) -> int:
        print(f'Scan: "{text}"')

        result = 0

        current_states: List[MutableState] = []
        next_states: List[MutableState] = []

        for char in text:
            while current_states:
                print(current_states)

                current_state = current_states.pop()
                node = current_state.node[char]

                if not node:  # go without carry
                    ...
                elif node.terminator:  # word found!
                    result += node.weight
                    print(f'+{node.weight} ET: {current_state.node.value} -> {node.value} (carry: {list(current_state.carry_queue)})')
                    print(self.root.prettify())

                    node.terminator = False

                    # Decrease weights of a subtree
                    visited: Node = node
                    while not isinstance(visited, RootNode):
                        visited.weight -= 1
                        visited = visited.parent

                    next_state = MutableState(
                        node=node,
                        carry_queue=copy.copy(current_state.carry_queue),
                        carry_index=copy.copy(current_state.carry_index),
                    )

                    next_states.append(next_state)
                else:  # im node
                    print(f'IT: {current_state.node.value} -> {node.value} (carry: {list(current_state.carry_queue)})')

                    next_state = MutableState(
                        node=node,
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

            if char in self.root:
                new_state = MutableState(node)
                next_states.append(new_state)
                print(f'ST: * -> {node.value}')

            current_states, next_states = next_states, []

        print(current_states)
        print(result)
        return result
