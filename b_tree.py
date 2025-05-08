""" B-tree """

class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(True)
        self.t = t

    def insert(self, k):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode(leaf=False)
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, k)
        else:
            self.insert_non_full(root, k)

    def insert_non_full(self, x, k):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self.split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self.insert_non_full(x.children[i], k)

    def split_child(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(leaf=y.leaf)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        x.children.insert(i + 1, z)

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1
        if i < len(node.keys) and k == node.keys[i]:
            return (node, i)
        if node.leaf:
            return None
        return self.search(k, node.children[i])

    def delete(self, k):
        if not self.root:
            return
        self._delete(self.root, k)

        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, k):
        t = self.t

        i = 0
        while i < len(node.keys) and k > node.keys[i]:
            i += 1

        if i < len(node.keys) and k == node.keys[i]:
            if node.leaf:
                node.keys.pop(i)
                return

            else:
                if len(node.children[i].keys) >= t:
                    pred = self._get_predecessor(node, i)
                    node.keys[i] = pred
                    self._delete(node.children[i], pred)

                elif len(node.children[i + 1].keys) >= t:
                    succ = self._get_successor(node, i)
                    node.keys[i] = succ
                    self._delete(node.children[i + 1], succ)

                else:
                    self._merge_children(node, i)
                    self._delete(node.children[i], k)

        else:
            if node.leaf:
                return

            child_index = i

            if child_index < len(node.children) and len(node.children[child_index].keys) < t:
                self._fill_child(node, child_index)

            if child_index >= len(node.children):
                child_index = len(node.children) - 1

            self._delete(node.children[child_index], k)

    def _get_predecessor(self, node, index):

        curr = node.children[index]
        while not curr.leaf:
            curr = curr.children[-1]
        return curr.keys[-1]

    def _get_successor(self, node, index):

        curr = node.children[index + 1]
        while not curr.leaf:
            curr = curr.children[0]
        return curr.keys[0]

    def _merge_children(self, node, index):

        left_child = node.children[index]
        right_child = node.children[index + 1]

        left_child.keys.append(node.keys[index])

        left_child.keys.extend(right_child.keys)
        if not left_child.leaf:
            left_child.children.extend(right_child.children)

        node.keys.pop(index)
        node.children.pop(index + 1)

    def _fill_child(self, node, index):

        if index > 0 and len(node.children[index - 1].keys) >= self.t:
            self._borrow_from_prev(node, index)

        elif index < len(node.children) - 1 and len(node.children[index + 1].keys) >= self.t:
            self._borrow_from_next(node, index)

        else:
            if index == len(node.children) - 1:
                self._merge_children(node, index - 1)
            else:
                self._merge_children(node, index)

    def _borrow_from_prev(self, node, index):

        child = node.children[index]
        sibling = node.children[index - 1]

        child.keys.insert(0, node.keys[index - 1])

        node.keys[index - 1] = sibling.keys.pop()

        if not sibling.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_next(self, node, index):

        child = node.children[index]
        sibling = node.children[index + 1]

        child.keys.append(node.keys[index])

        node.keys[index] = sibling.keys.pop(0)

        if not sibling.leaf:
            child.children.append(sibling.children.pop(0))

    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        i = 0
        while i < len(node.keys):
            if not node.leaf:
                self._inorder_traversal(node.children[i], result)
            result.append(node.keys[i])
            i += 1
        if not node.leaf and node.children:
            self._inorder_traversal(node.children[-1], result)

    def preorder_traversal(self):
        result = []
        self._preorder_traversal(self.root, result)
        return result

    def _preorder_traversal(self, node, result):
        if node:
            result.extend(node.keys)
            if not node.leaf:
                for child in node.children:
                    self._preorder_traversal(child, result)
