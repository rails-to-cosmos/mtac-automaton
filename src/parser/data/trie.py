from __future__ import annotations

import math
import dataclasses

from typing import Optional

from parser.utils.text import normalize_word


@dataclasses.dataclass
class Node:
    value: str = dataclasses.field(default='')
    depth: int = dataclasses.field(default=0)
    parent: Optional[Node] = None
    children: dict[str, Node] = dataclasses.field(default_factory=dict)
    weight: int = dataclasses.field(default=1)
    terminator: bool = False

    def __getitem__(self, key: str) -> Node:
        return self.children[key]

    def __setitem__(self, key: str, value: Node) -> None:
        self.children[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.children


@dataclasses.dataclass
class RootNode(Node):
    def prettify(root: RootNode) -> str:
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

            if node:
                result.append('- ' + node.value + ' ' + f'({node.depth}, {node.weight})')

            for child in node.children.values():
                stack.append((depth + TOKEN_LEN, child))

        return ' '.join(result)
