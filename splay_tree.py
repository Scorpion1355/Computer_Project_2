""" Splay Tree """

class Node:

    def __init__(self, key):

        self.key = key
        self.left = None
        self.right = None
        self.parent = None

class SplayTree:

    def __init__(self):

        self.root = None

    def rotate_left(self, x):

        y = x.right
        if y is None:
            return

        x.right = y.left
        if y.left:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def rotate_right(self, x):

        y = x.left
        if y is None:
            return

        x.left = y.right
        if y.right:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def splay(self, x):

        while x.parent:
            if x.parent.parent is None:
                if x == x.parent.left:
                    self.rotate_right(x.parent)
                else:
                    self.rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                self.rotate_right(x.parent.parent)
                self.rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                self.rotate_left(x.parent.parent)
                self.rotate_left(x.parent)
            else:
                if x == x.parent.left:
                    self.rotate_right(x.parent)
                    self.rotate_left(x.parent)
                else:
                    self.rotate_left(x.parent)
                    self.rotate_right(x.parent)

    def subtree_minimum(self, x):

        while x.left:
            x = x.left
        return x

    def insert(self, key):

        node = self.root
        parent = None

        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self.splay(node)
                return

        new_node = Node(key)
        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self.splay(new_node)

    def find(self, key):

        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return None

    def search(self, key):

        node = self.find(key)
        if node:
            self.splay(node)
        return node

    def delete(self, key):

        node = self.find(key)
        if node is None:
            return

        self.splay(node)

        if node.left:
            left_subtree = node.left
            left_subtree.parent = None
        else:
            left_subtree = None

        if node.right:
            right_subtree = node.right
            right_subtree.parent = None
        else:
            right_subtree = None

        if left_subtree:
            max_node = self.subtree_minimum(left_subtree)
            self.splay(max_node)
            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node
            self.root = max_node
        else:
            self.root = right_subtree

    def inorder(self, node, res):

        if not node:
            return None
        self.inorder(node.left, res)
        res.append(node.key)
        self.inorder(node.right, res)

    def preorder(self, node, res):

        if not node:
            return None
        res.append(node.key)
        self.preorder(node.left, res)
        self.preorder(node.right, res)
