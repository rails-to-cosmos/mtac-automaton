from __future__ import annotations

from typing import *
from dataclasses import dataclass


class Char:
    value: str


class Node:
    children: dict[str, Node]

    def __init__(self) -> None:
        self.children = dict()

    def __repr__(self) -> str:
        result = []
        for child in self.children:
            result.append(f' - {child}')
        return '*' + '\n '.join(result)


class RootNode(Node):
    ...


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

    def add_word(self, word: str) -> None:
        current_node: Node = self.root
        depth = len(word)

        for index, char in enumerate(word):
            if char in current_node.children:
                match current_node:
                    case IntermediateNode():
                        current_node.depth = max(current_node.depth, depth)

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
automaton.add_word('bpd')

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
