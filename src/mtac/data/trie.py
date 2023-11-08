from __future__ import annotations

import math

from dataclasses import dataclass, field
from collections import deque
from typing import Optional, Dict, List, Tuple
from copy import deepcopy

from mtac.utils.text import normalize_word


@dataclass
class Carry:
    # carrying sliding window with index for lookup optimization
    size: int = 0
    queue: deque = field(default_factory=deque)
    index: Dict[str, int] = field(default_factory=dict)

    def adjust(self) -> None:
        while self.is_full():
            item, *_ = self.queue
            self.remove(item)

    def remove(self, item: str) -> None:
        self.queue.remove(item)
        self.index[item] -= 1
        if self.index[item] == 0:
            del self.index[item]

    def add(self, item: str) -> None:
        self.adjust()
        self.queue.append(item)
        if item not in self.index:
            self.index[item] = 0
        self.index[item] += 1

    def is_full(self) -> bool:
        return len(self.queue) >= self.size

    def __contains__(self, key: str) -> bool:
        return key in self.index


@dataclass
class Node:
    value: str = field(default='*')
    parent: Optional[Node] = None
    children: dict[str, Node] = field(default_factory=dict)
    weight: int = field(default=1)
    terminator: bool = False
    carry: Carry = field(default_factory=Carry)

    @property
    def depth(self) -> int:
        return self.carry.size

    @depth.setter
    def depth(self, value):
        self.carry.size = value

    def __getitem__(self, key: str) -> Node:
        return self.children[key]

    def __setitem__(self, key: str, value: Node) -> None:
        self.children[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.children

    def __repr__(self) -> str:
        return f'State({self.value}, {list(self.carry.queue)})'

    def __str__(self) -> str:
        return f'{self.value} ({list(self.carry.queue)})'

    def terminate(self) -> int:
        if not self.terminator:
            return 0

        result = self.weight
        self.terminator = False

        permutation = []
        node = self
        while node.parent:
            permutation.append(node.value)
            node.weight -= 1
            node = node.parent

        print(f'! Match found: {self.value}, permutation: {"".join(reversed(permutation))}')

        return result

    def is_active(self) -> bool:
        return self.weight > 0

    def goto(self, key: str) -> Tuple[List[Node], int]:
        "Perform state transition. This could result in a bunch of the new states."

        transitions: List[Node] = []
        matches: int = 0

        if not self.is_active():
            return transitions, matches
        elif key not in self:
            if not self.carry.is_full():
                transitions.append(self)

            self.fail(key)
        elif not self[key].is_active():
            ...
        else:  # can proceed with the state transition
            # print(f'Key {key} found in {list(self.children.keys())}: proceed with the state transition')

            state = self[key]
            matches += state.terminate()
            transitions.append(state)
            transitions.extend(state.goto_carry())

        return (transitions, matches)

    def goto_carry(self) -> List[Node]:
        """
        Performs depth-first search using it's own carry buffer.

        """

        transitions: List[Node] = []

        if not self.is_active():
            return transitions

        dfsq: List[Node] = []
        for child in self.children.values():
            dfsq.append(child)

        while dfsq:
            node = dfsq.pop()

            if not node.is_active():
                continue

            if node.value in node.carry:
                node.carry.remove(node.value)
                transitions.append(node)
                for child in node.children.values():
                    dfsq.append(child)

        return transitions


    def fail(self, key: str) -> None:
        # lookup failed, memorize carry in-depth
        # print(f'Key {key} not found in {list(self.children.keys())}')
        # print(f'Update carries in-depth')

        if not self.is_active():
            return

        dfsq = [self]
        while dfsq:
            node = dfsq.pop()

            if not node.is_active():
                continue

            node.carry.add(key)
            # print(f'Carry updated: {node}')
            for child in node.children.values():
                dfsq.append(child)

@dataclass
class RootNode(Node):
    def goto(self, key: str) -> Tuple[List[Node], int]:
        "Perform state transition. This could result in a bunch of new states."

        transitions: List[Node] = [self]  # always preserve root in transitions
        matches = 0

        if key in self:
            state = self[key]
            transitions.append(state)
            matches += state.terminate()

        return transitions, matches

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
                result.append(f'- {node.value} ({node.depth}, {node.weight})')

            for child in node.children.values():
                stack.append((depth + TOKEN_LEN, child))

        return ' '.join(result)
