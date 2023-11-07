from typing import Dict

from collections import deque
from dataclasses import dataclass
from dataclasses import field

from parser.data.tree import InterimNode
from parser.data.tree import EndNode


@dataclass
class MutableState:
    node: InterimNode | EndNode

    # carrying sliding window with index for lookup optimization
    carry_queue: deque = field(default_factory=deque)
    carry_index: Dict[str, int] = field(default_factory=dict)

    def carry(self, item: str) -> None:
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
        return f'S({self.node.value}, {list(self.carry_queue)})'
