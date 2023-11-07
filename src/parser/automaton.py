from typing import List
from typing import Dict

import logging
import dataclasses
import copy

from collections import deque
from dataclasses import dataclass, field

from parser.data.tree import RootNode, EndNode, InterimNode, Node
from parser.utils.text import normalize_word


@dataclass
class State:
    node: InterimNode | EndNode
    carry_queue: deque = field(default_factory=deque)  # lookups can be optimized with set
    carry_index: Dict[str, int] = field(default_factory=dict)

    def remember(self, item: str) -> None:
        self.adjust()
        self.carry_queue.append(item)
        if item not in self.carry_index:
            self.carry_index[item] = 0
        self.carry_index[item] += 1

    def adjust(self) -> None:
        while len(self.carry_queue) >= self.node.depth:
            item, *_ = self.carry_queue
            self.remove(item)

    def remove(self, item: str) -> None:
        self.carry_queue.remove(item)
        self.carry_index[item] -= 1
        if self.carry_index[item] == 0:
            del self.carry_index[item]

    def __repr__(self) -> str:
        return f'State({self.node.value}, {self.carry_queue})'


class Automaton:
    def __init__(self) -> None:
        self.root: RootNode = RootNode()

    def validate_input(self, s: str) -> None:
        ...

    def validate_dictionary(self, s: str) -> None:
        ...

    def scan(self, text: str) -> int:
        print(f'Scan "{text}"')

        result = 0

        active_states: List[State] = []
        next_states: List[State] = []

        for char in text:

            while active_states:
                state = active_states.pop()

                if char not in state.node:
                    state.remember(char)
                    next_states.append(state)
                    continue

                match state.node[char]:
                    case EndNode(depth=depth, factor=factor) as end_node:  # Word found!
                        result += factor
                        print(f'State transition: {state.node.value} -> {end_node.value} (carry: {state.carry_queue})')
                        state.node = end_node
                        end_node.factor = 0  # TODO Update node type / write it to (seen) / remove all factor 0
                    case InterimNode() as im_node:
                        print(f'State transition: {state.node.value} -> {im_node.value} (carry: {state.carry_queue})')
                        state.node = im_node

                carry_states = [state]
                while carry_states:
                    carry_state = carry_states.pop()

                    trans = False
                    for child in carry_state.node.children.values():
                        if child.value in state.carry_index:
                            new_state = State(
                                node=child,
                                carry_queue=copy.copy(state.carry_queue),
                                carry_index=copy.copy(state.carry_index),
                            )

                            new_state.remove(child.value)
                            carry_states.append(new_state)

                            print(f'State transition: {state.node.value} -> {new_state.node.value} (carry: {new_state.carry_queue})')
                            trans = True

                    if not trans:
                        next_states.append(carry_state)

            match self.root[char]:
                case InterimNode() | EndNode() as node:
                    state = State(node)
                    next_states.append(state)
                    print(f'State transition: * -> {state.node.value}')

            active_states, next_states = next_states, []

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
