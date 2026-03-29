#!/usr/bin/env python3
"""Rope data structure for efficient string operations."""
import sys

class RopeNode:
    def __init__(self, text=None, left=None, right=None):
        if text is not None:
            self.text, self.left, self.right = text, None, None
            self.weight = len(text)
        else:
            self.text, self.left, self.right = None, left, right
            self.weight = _length(left)
    def is_leaf(self): return self.text is not None

def _length(node):
    if node is None: return 0
    if node.is_leaf(): return len(node.text)
    return _length(node.left) + _length(node.right)

def index(node, i):
    if node is None: raise IndexError
    if node.is_leaf(): return node.text[i]
    if i < node.weight: return index(node.left, i)
    return index(node.right, i - node.weight)

def concat(a, b):
    if a is None: return b
    if b is None: return a
    return RopeNode(left=a, right=b)

def split(node, i):
    if node is None: return None, None
    if node.is_leaf():
        return (RopeNode(node.text[:i]), RopeNode(node.text[i:])) if i < len(node.text) else (node, None)
    if i < node.weight:
        left_l, left_r = split(node.left, i)
        return left_l, concat(left_r, node.right)
    elif i > node.weight:
        right_l, right_r = split(node.right, i - node.weight)
        return concat(node.left, right_l), right_r
    else:
        return node.left, node.right

def to_string(node):
    if node is None: return ""
    if node.is_leaf(): return node.text
    return to_string(node.left) + to_string(node.right)

def insert(node, i, text):
    left, right = split(node, i)
    return concat(concat(left, RopeNode(text)), right)

def delete(node, i, length):
    left, rest = split(node, i)
    _, right = split(rest, length)
    return concat(left, right)

def main():
    if len(sys.argv) < 2: print("Usage: rope_string.py <demo|test>"); return
    if sys.argv[1] == "test":
        r = RopeNode("Hello, ")
        r2 = concat(r, RopeNode("World!"))
        assert to_string(r2) == "Hello, World!"
        assert _length(r2) == 13
        assert index(r2, 0) == "H"; assert index(r2, 7) == "W"
        r3 = insert(r2, 7, "Beautiful ")
        assert to_string(r3) == "Hello, Beautiful World!"
        r4 = delete(r3, 7, 10)
        assert to_string(r4) == "Hello, World!"
        left, right = split(RopeNode("abcdef"), 3)
        assert to_string(left) == "abc"; assert to_string(right) == "def"
        assert to_string(concat(None, RopeNode("x"))) == "x"
        print("All tests passed!")
    else:
        r = concat(RopeNode("Hello"), RopeNode(" World"))
        print(f"Rope: {to_string(r)}, len={_length(r)}")

if __name__ == "__main__": main()
