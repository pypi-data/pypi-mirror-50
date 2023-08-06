"""Algorithms for maintaing red-black trees.

A red-black tree is a binary search tree that satisfies the following
properties.
-   Each node is either red or black.
-   The root node is black.
-   A red node must have a black parent.
-   For any subtree, every simple path from the root of the subtree to a
    leaf contains the same number of black nodes as any other path.
"""

import enum

class Color(enum.Enum):
    """Node.Color is either RED or BLACK."""
    BLACK = enum.auto()
    RED = enum.auto()

class Node:
    """An instance represents a node in a red-black tree."""

    def __init__(self, key, color=Color.RED):
        self.key = key
        self.color = color
        self.parent = None
        self.left = None
        self.right = None
        self.value = None

    def __repr__(self):
        return "<Node {} {} {} {} {} object at {}>".format(
            self.key,
            self.color,
            self.parent,
            self.left,
            self.right,
            id(self)
        )

def rotate_left(root, x):
    """Apply left rotation on x, and return the new root."""
    assert root and x and x.right
    y = x.right

    x.right = y.left
    if x.right:
        x.right.parent = x

    y.left = x
    y.parent = x.parent
    x.parent = y

    if not y.parent:
        root = y
    elif y.parent.left == x:
        y.parent.left = y
    elif y.parent.right == x:
        y.parent.right = y
    return root

def rotate_right(root, y):
    """Apply right rotation on y, and return the new root."""
    assert root and y and y.left
    x = y.left

    y.left = x.right
    if y.left:
        y.left.parent = y

    x.right = y
    x.parent = y.parent
    y.parent = x

    if not x.parent:
        root = x
    elif x.parent.right == y:
        x.parent.right = x
    elif x.parent.left == y:
        x.parent.left = x
    return root

def repair(root, node):
    """Restore red-black properties after inserting, and return new root."""
    if not root or not node:
        return root

    parent = node.parent
    if parent and parent.color == Color.RED:
        grandparent = parent.parent
        uncle = None
        if grandparent:
            if grandparent.left == parent:
                uncle = grandparent.right
            else:
                uncle = grandparent.left

        if uncle and uncle.color == Color.RED:
            grandparent.color = Color.RED
            parent.color = Color.BLACK
            uncle.color = Color.BLACK
            return repair(root, grandparent)
        if grandparent:
            if grandparent.left == parent and parent.right == node:
                root = rotate_left(root, parent)
            elif grandparent.right == parent and parent.left == node:
                root = rotate_right(root, parent)

            if grandparent.left == parent and parent.left == node:
                parent.color = Color.BLACK
                grandparent.color = Color.RED
                root = rotate_right(root, grandparent)
            elif grandparent.right == parent and parent.right == node:
                parent.color = Color.BLACK
                grandparent.color = Color.RED
                root = rotate_left(root, grandparent)

    root.color = Color.BLACK
    return root

def insert(root, node):
    """Insert node into red-black tree rooted at root.

    Returns the new root, and a boolean that tells if the tree got larger.
    """
    if not node:
        return root, False

    node.left = None
    node.right = None
    node.parent = None
    if not root:
        node.color = Color.BLACK
        return node, True

    node.color = Color.RED
    closest = closest_match(root, node.key)
    if closest.key == node.key:
        # replace closest with node
        node.color = closest.color
        node.left = closest.left
        node.right = closest.right
        node.parent = closest.parent
        if node.left:
            node.left.parent = node
        if node.right:
            node.right.parent = node
        if not node.parent:
            root = node
        elif node.parent.left == closest:
            node.parent.left = node
        else:
            node.parent.right = node
    else:
        node.parent = closest
        if node.key < closest.key:
            closest.left = node
        else:
            closest.right = node
    return repair(root, node), (closest.key != node.key)

def closest_match(root, key):
    """Return node in tree with closest matching key.

    The return value is either a node with the same key, or a node that would
    be the parent if a node for the key is inserted.
    """
    parent = None
    child = root
    while child and child.key != key:
        parent = child
        child = child.left if key < child.key else child.right
    return child if child else parent

def search(root, key):
    """Return node with matching key, or None."""
    node = root
    while node and node.key != key:
        node = node.left if key < node.key else node.right
    return node

def minimum(root):
    """Return node with smallest key in the tree at given root."""
    if not root:
        return None
    while root.left:
        root = root.left
    return root

def maximum(root):
    """Return node with largest key in the tree at given root."""
    if not root:
        return None
    while root.right:
        root = root.right
    return root

def successor(node):
    """Return inorder successor of node."""
    if not node:
        return None
    if node.right:
        return minimum(node.right)
    child = node
    parent = child.parent
    while parent and parent.left != child:
        child = parent
        parent = parent.parent
    return parent

def predecessor(node):
    """Return inorder predecessor of node."""
    if not node:
        return None
    if node.left:
        return maximum(node.left)
    child = node
    parent = child.parent
    while parent and parent.right != child:
        child = parent
        parent = parent.parent
    return parent

def iterator(root):
    """Generate keys (or key-value pairs) in the tree."""
    node = minimum(root)
    while node:
        if node.value is not None:
            yield (node.key, node.value)
        else:
            yield node.key
        node = successor(node)

def reversed_iterator(root):
    """Generate keys (or key-value pairs) in reversed order."""
    node = maximum(root)
    while node:
        if node.value is not None:
            yield (node.key, node.value)
        else:
            yield node.key
        node = predecessor(node)
