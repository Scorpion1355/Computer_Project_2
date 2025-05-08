""" Tree Adaptor """

from abstract_class import SelfBalancingTree
from AVL_Tree import AVLTree
from red_black_tree import RedBlackTree
from splay_tree import SplayTree
from b_tree import BTree
from two_three_tree import TwoThreeTree

class AVLTreeAdapter(SelfBalancingTree):

    def __init__(self):

        self.tree = AVLTree()

    def insert(self, key):

        self.tree.insert(key)

    def delete(self, key):

        self.tree.delete(key)

    def search(self, key):

        return self.tree.search(key)

    def inorder_traversal(self):

        return list(self.tree.in_order())

    def preorder_traversal(self):

        return list(self.tree.pre_order())

    def is_empty(self):

        return self.tree.root is None

class RedBlackTreeAdapter(SelfBalancingTree):

    def __init__(self):

        self.tree = RedBlackTree()

    def insert(self, key):

        self.tree.insert(key)

    def delete(self, key):

        self.tree.delete(key)

    def search(self, key):

        return self.tree.search(key) is not None

    def inorder_traversal(self):

        return self.tree.inorder_walk()

    def preorder_traversal(self):

        return self.tree.preorder_walk()

    def is_empty(self):

        return self.tree.root == self.tree.NIL

class SplayTreeAdapter(SelfBalancingTree):

    def __init__(self):

        self.tree = SplayTree()

    def insert(self, key):

        self.tree.insert(key)

    def delete(self, key):

        self.tree.delete(key)

    def search(self, key):

        return self.tree.search(key) is not None

    def inorder_traversal(self):

        result = []
        self.tree.inorder(self.tree.root, result)
        return result

    def preorder_traversal(self):

        result = []
        self.tree.preorder(self.tree.root, result)
        return result

    def is_empty(self):

        return self.tree.root is None

class BTreeAdapter(SelfBalancingTree):

    def __init__(self, degree=3):

        self.tree = BTree(degree)

    def insert(self, key):

        self.tree.insert(key)

    def delete(self, key):

        self.tree.delete(key)

    def search(self, key):

        return self.tree.search(key) is not None

    def inorder_traversal(self):

        return self.tree.inorder_traversal()

    def preorder_traversal(self):

        return self.tree.preorder_traversal()

    def is_empty(self):

        return self.tree.root is None or len(self.tree.root.keys) == 0

class TwoThreeTreeAdapter(SelfBalancingTree):

    def __init__(self):

        self.tree = TwoThreeTree()

    def insert(self, key):

        self.tree.insert(key)

    def delete(self, key):

        self.tree.delete(key)

    def search(self, key):

        return self.tree.search(key)

    def inorder_traversal(self):

        return self.tree.inorder()

    def preorder_traversal(self):

        return self.tree.preorder()

    def is_empty(self):

        return self.tree.root is None or not self.tree.root.keys
