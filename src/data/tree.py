from __future__ import annotations

import math
from typing import *
from dataclasses import dataclass

from src.utils.text import normalize_word


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
