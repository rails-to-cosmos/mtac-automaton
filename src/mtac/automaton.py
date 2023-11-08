from typing import List

from mtac.data.trie import Node
from mtac.data.trie import RootNode
from mtac.utils.text import normalize_word


class Automaton:
    def __init__(self) -> None:
        self.root: RootNode = RootNode()

    def add_word(self, word: str) -> None:
        normalized_word = normalize_word(word)
        word_depth = len(normalized_word)  # word depth determines a carry size

        current_node: Node = self.root
        for index, char in enumerate(normalized_word):
            is_term_char = index == word_depth - 1

            if char in current_node.children:  # char has already been visited
                child = current_node[char]
                max_depth = max(child.depth, word_depth)
                child.weight += 1
                child.terminator = child.terminator or is_term_char
            else:
                max_depth = max(current_node.depth, word_depth)

                child = Node(
                    parent=current_node,
                    value=char,
                    terminator=is_term_char,
                )

                current_node[char] = child

            child.depth = max_depth
            current_node = child

    def scan(self, text: str) -> int:
        print(f'Scan: "{text}"')

        result = 0

        active_states: List[Node] = [self.root]
        state_buffer: List[Node] = []

        for char in text:
            print('---')
            print(f'Char: {char}')
            while active_states:
                state = active_states.pop()
                new_states, matches = state.goto(char)
                state_buffer.extend(new_states)
                result += matches
            # print(f'States ({len(state_buffer)}):')
            # for state in state_buffer:
            #     print(f'- {str(state)}')
            active_states, state_buffer = state_buffer, []

        print(f'Result: {result}')
        return result
