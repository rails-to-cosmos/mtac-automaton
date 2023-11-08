# from __future__ import annotations

# import math

# from dataclasses import dataclass, field
# from collections import deque
# from typing import Optional, Dict, List
# from copy import deepcopy

# from mtac.utils.text import normalize_word


# @dataclass
# class Carry:
#     # carrying sliding window with index for lookup optimization
#     size: int = 0
#     queue: deque = field(default_factory=deque)
#     index: Dict[str, int] = field(default_factory=dict)

#     def adjust(self) -> None:
#         while self.is_full():
#             item, *_ = self.queue
#             self.remove(item)

#     def remove(self, item: str) -> None:
#         self.queue.remove(item)
#         self.index[item] -= 1
#         if self.index[item] == 0:
#             del self.index[item]

#     def add(self, item: str) -> None:
#         self.adjust()
#         self.queue.append(item)
#         if item not in self.index:
#             self.index[item] = 0
#         self.index[item] += 1

#     def is_full(self) -> bool:
#         return len(self.queue) >= self.size

#     def __contains__(self, key: str) -> bool:
#         return key in self.index


# @dataclass
# class Node:
#     value: str = field(default='*')
#     parent: Optional[Node] = None
#     children: dict[str, Node] = field(default_factory=dict)
#     weight: int = field(default=1)
#     terminator: bool = False
#     carry: Carry = field(default_factory=Carry)

#     matches: int = 0

#     @property
#     def depth(self) -> int:
#         return self.carry.size

#     @depth.setter
#     def depth(self, value):
#         self.carry.size = value

#     def __getitem__(self, key: str) -> Node:
#         return self.children[key]

#     def __setitem__(self, key: str, value: Node) -> None:
#         self.children[key] = value

#     def __contains__(self, key: str) -> bool:
#         return key in self.children

#     def __repr__(self) -> str:
#         return f'State({self.value}, {list(self.carry.queue)})'

#     def __str__(self) -> str:
#         return f'{self.value} ({list(self.carry.queue)})'

#     def terminate(self) -> int:
#         if not self.is_active():
#             return 0

#         if not self.terminator:
#             return 0

#         result = self.weight
#         self.terminator = False

#         permutation = []
#         node = self
#         while node.parent:
#             permutation.append(node.value)
#             node.weight -= 1
#             node = node.parent

#         print(f'! Match found: {self.value}, permutation: {"".join(reversed(permutation))}')

#         return result

#     def is_active(self) -> bool:
#         return self.weight > 0

#     def goto(self, key: str) -> List[Node]:
#         "Perform state transition. This could result in a bunch of the new states."

#         transitions: List[Node] = []

#         if not self.is_active():
#             return transitions

#         if key not in self:
#             if not self.carry.is_full():
#                 transitions.append(self)
#             self.carry.add(key)
#             return transitions

#         if self.terminator:
#             self.matches += self.terminate()

#         # if len(self.children) > 1:
#         transitions.append(self)
#         transitions.append(self[key])
#         # transitions.extend(self.goto_carry())

#         return transitions

#     def goto_carry(self) -> List[Node]:
#         """
#         Performs depth-first search following it's own carry buffer.

#         """

#         transitions: List[Node] = []

#         if not self.is_active():
#             return transitions

#         dfsq: List[Node] = list(self.children.values())

#         while dfsq:
#             node = dfsq.pop()

#             if not node.is_active():
#                 continue

#             if node.value in node.parent.carry:
#                 node.carry = deepcopy(node.parent.carry)
#                 node.carry.remove(node.value)
#                 transitions.append(node)

#                 for child in node.children.values():
#                     dfsq.append(child)

#         return transitions

#     # def carry_downstream(self, key: str) -> None:
#     #     if not self.is_active():
#     #         return

#     #     dfsq = list(self.children.values())

#     #     while dfsq:
#     #         node = dfsq.pop()

#     #         if not node.is_active():
#     #             continue

#     #         node.carry.add(key)
#     #         for child in node.children.values():
#     #             dfsq.append(child)

# @dataclass
# class RootNode(Node):
#     def goto(self, key: str) -> List[Node]:
#         "Perform state transition. This could result in a bunch of new states."

#         transitions: List[Node] = [self]  # always preserve root in transitions
#         matches = 0

#         if key in self:
#             # print(f'Key {key} found in {list(self.children.keys())}: proceed with the state transition')

#             state = self[key]
#             transitions.append(state)
#             matches += state.terminate()

#         return transitions

#     def prettify(root: RootNode) -> str:
#         # some constants for pretty printing tree structures
#         ROOT_SYMBOL = '*'
#         TAB_SYMBOL = ' '
#         TOKEN_LEN = 11

#         result = [ROOT_SYMBOL]
#         prev_depth = math.inf

#         stack = [(1, child) for child in root.children.values()]

#         while stack:
#             depth, node = stack.pop()

#             if prev_depth >= depth:
#                 result.append('\n' + TAB_SYMBOL * depth)

#             prev_depth = depth

#             if node:
#                 if node.terminator:
#                     result.append(f'> {node.value} ({node.depth}, {node.weight})')
#                 else:
#                     result.append(f'- {node.value} ({node.depth}, {node.weight})')

#             for child in node.children.values():
#                 stack.append((depth + TOKEN_LEN, child))

#         return ' '.join(result)
