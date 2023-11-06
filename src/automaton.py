from __future__ import annotations

import functools as ft

import math
from typing import *
from dataclasses import dataclass


class Char:
    value: str


class Node:
    children: dict[str, IntermediateNode]

    def __init__(self) -> None:
        self.children = dict()


class RootNode(Node):
    def pretty(self) -> list[str]:
        ROOT_SYMBOL = '*'
        TAB_SYMBOL = ' '
        TOKEN_LEN = 6

        result = [ROOT_SYMBOL]
        prev_depth = math.inf

        stack = [(1, child) for child in self.children.values()]

        while stack:
            depth, node = stack.pop()

            if prev_depth >= depth:
                result.append('\n' + TAB_SYMBOL * depth)

            prev_depth = depth
            match node:
                case EndNode():
                    result.append(node.value + '!' + f'({node.depth})')
                case _:
                    result.append(node.value + ' ' + f'({node.depth})')

            for child in node.children.values():
                stack.append((depth + TOKEN_LEN, child))

        return result


class IntermediateNode(Node):
    value: str
    depth: int

    def __init__(self, value: str, depth: int) -> None:
        super().__init__()
        self.value = value
        self.depth = depth


class EndNode(IntermediateNode):
    ...


class Automaton:
    root: RootNode

    def __init__(self) -> None:
        self.root = RootNode()

    @ft.cache
    def normalize_word(self, word: str) -> str:
        if len(word) <= 3:
            return word

        return word[0] + ''.join(sorted(word[1:len(word) - 1])) + word[-1]

    def add_word(self, word: str) -> None:
        normalized_word = self.normalize_word(word)  # compaction

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
                new_node: Node

                if index == depth - 1:
                    new_node = EndNode(char, depth)
                else:
                    new_node = IntermediateNode(char, depth)

                current_node.children[char] = new_node
                current_node = new_node

automaton = Automaton()
automaton.add_word('aapxj')
automaton.add_word('apaxj')
automaton.add_word('apaxd')
automaton.add_word('apal')
automaton.add_word('pda')
automaton.add_word('bpd')
automaton.add_word('bp')
automaton.add_word('bzd')
automaton.add_word('b')

print(' '.join(automaton.root.pretty()))

# class MTACAutomaton:
#     alphabet: int
#     root: State

#     patterns: list[list[str]]
#     PPA: list[list[str]]
#     TPA: list[str]

#     def __init__(self, alpha: int) -> None:
#         self.alphabet = alpha

#     def add_pattern(self, p: str) -> None:
#         self.patterns.append(p)
#         self.PPA.append(self.create_pa(p))

#     def calc_ac_automaton(self) -> None:
#         root = State()
#         self.calc_goto_func()
#         self.calc_fail_func()

#     def calc_goto_func(self) -> None:
#         for i in range(len(self.patterns)):
#             p = self.patterns[i]
#             M = len(p)
#             m = len(p[0])
#             active_state = self.root

#             for k in range(m):
#                 trans = self.get_column(p, k, self.PPA[i], 0)

#                 if active_state.child.find()
