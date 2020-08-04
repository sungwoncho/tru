# generate_coding.py generates a prefix-free variable-length code
# for the given set of operations using Huffman coding

from heapq import heappush, heappop
from functools import total_ordering

@total_ordering
class Node():
    def __init__(self, priority, value, left, right):
        self.priority = priority
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.priority == other.priority

    def __lt__(self, other):
        if not isinstance(other, type(self)): return NotImplemented
        return self.priority < other.priority

ops = [
    # utils
    "print-utf8",
    "print-int",
    "input-utf8",
    "input-int",
    # stack
    "toggle-stack",
    "pop-move",
    "pop-discard",
    "dup",
    "swap",
    # arithmetic
    "sub",
    "add",
    # logic
    "gt",
    "eq",
    "not",
    # flow
    "end",
]

# [] label definition
# () push
# {} if-goto label
# [0](9)(98)(2)(8)<><<<><><<><>{0}

def build_trie():
    pq = []

    for idx, op in enumerate(ops):
        heappush(pq, Node(idx, op, None, None))

    while (len(pq) > 1):
        x = heappop(pq)
        y = heappop(pq)

        heappush(pq, Node(x.priority + y.priority, "", x, y))

    return heappop(pq)

def build_code(st, node, acc):
    if (node == None):
        return
    if (node.left == None and node.right == None):
        st[node.value] = acc

    build_code(st, node.left, acc + "<")
    build_code(st, node.right, acc + ">")

if __name__ == '__main__':
    root = build_trie()
    st = {}
    build_code(st, root, "")

    print("=========== PAREN CODE ===========")
    for op in ops:
        print(f"{op} {st[op]}")
