""" AVL Tree implementation """

class Node:

    def __init__(self, key):

        self.key = key
        self.height = 1
        self.left = None
        self.right = None

    def update_height(self):

        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = 1 + max(left_height, right_height)
        return self

    def balance_factor(self):

        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        return left_height - right_height

    def __repr__(self):

        return f"Node(key={self.key}, height={self.height})"


class AVLTree:

    def __init__(self):

        self.root = None

    def _rotate_right(self, node):

        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        node.update_height()
        return left_child.update_height()

    def _rotate_left(self, node):

        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        node.update_height()
        return right_child.update_height()

    def _balance_subtree(self, node):

        if not node:
            return None
        node.update_height()
        factor = node.balance_factor()
        if factor > 1:
            if node.left and node.left.balance_factor() < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if factor < -1:
            if node.right and node.right.balance_factor() > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key):

        def _insert(node, key):
            if not node:
                return Node(key)
            if key < node.key:
                node.left = _insert(node.left, key)
            elif key > node.key:
                node.right = _insert(node.right, key)
            return self._balance_subtree(node)
        self.root = _insert(self.root, key)

    def delete(self, key):

        def _delete(node, key):
            if not node:
                return None
            if key < node.key:
                node.left = _delete(node.left, key)
            elif key > node.key:
                node.right = _delete(node.right, key)
            else:
                if not (node.left and node.right):
                    return node.left or node.right
                successor = node.right
                while successor.left:
                    successor = successor.left
                node.key, successor.key = successor.key, node.key
                node.right = _delete(node.right, successor.key)
            return self._balance_subtree(node)
        self.root = _delete(self.root, key)

    def search(self, key):

        def _search(node, key):
            if not node:
                return False
            if key == node.key:
                return True
            return _search(node.left, key) if key < node.key else _search(node.right, key)
        return _search(self.root, key)

    def pre_order(self):

        def _preorder(node):
            if node:
                yield node.key
                yield from _preorder(node.left)
                yield from _preorder(node.right)
        yield from _preorder(self.root)

    def in_order(self):

        def _in_order(node):
            if node:
                yield from _in_order(node.left)
                yield node.key
                yield from _in_order(node.right)
        yield from _in_order(self.root)
