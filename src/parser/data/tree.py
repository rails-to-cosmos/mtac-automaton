from __future__ import annotations

import math
import dataclasses as dc
from typing import Optional

from parser.utils.text import normalize_word

@dc.dataclass
class Node:
    value: str = dc.field(default='')
    depth: int = dc.field(default=0)
    children: dict[str, InterimNode | EndNode] = dc.field(default_factory=dict)

    def __getitem__(self, key: str) -> Optional[Node]:
        return self.children.get(key)


@dc.dataclass
class RootNode(Node):
    ...


@dc.dataclass
class InterimNode(Node):
    ...


@dc.dataclass
class EndNode(Node):
    factor: int = dc.field(default=1)


def pretty(root: RootNode) -> str:
    # some constants for pretty printing tree structures
    ROOT_SYMBOL = '*'
    TAB_SYMBOL = ' '
    TOKEN_LEN = 11

    result = [ROOT_SYMBOL]
    prev_depth = math.inf

    stack = [(1, child) for child in root.children.values()]

    while stack:
        depth, node = stack.pop()

        if prev_depth >= depth:
            result.append('\n' + TAB_SYMBOL * depth)

        prev_depth = depth

        match node:
            case EndNode():
                result.append('- ' + node.value + ' ' + f'({node.depth}, {node.factor})')
            case InterimNode():
                result.append('- ' + node.value + ' ' + f'({node.depth}, 0)')

        for child in node.children.values():
            stack.append((depth + TOKEN_LEN, child))

    return ' '.join(result)
