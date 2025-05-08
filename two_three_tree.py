""" 2-3 tree implementation """

class Node:
    def __init__(self, keys=None, children=None):
        self.keys = keys or []
        self.children = children or []

    def is_leaf(self):
        return len(self.children) == 0

    def __repr__(self):
        return f"Node(keys={self.keys})"


class TwoThreeTree:
    def __init__(self):
        self.root = None

    def search(self, key, node=None):
        if node is None:
            node = self.root
        if node is None:
            return False
        for i, k in enumerate(node.keys):
            if key == k:
                return True
            if key < k:
                return self.search(key, node.children[i]) if node.children else False
        return self.search(key, node.children[-1]) if node.children else False

    def insert(self, key):
        if self.root is None:
            self.root = Node(keys=[key])
            return

        def _insert_rec(node, key):
            if node.is_leaf():
                node.keys.append(key)
                node.keys.sort()
            else:
                if key < node.keys[0]:
                    child_idx = 0
                elif len(node.keys) == 1 or key < node.keys[1]:
                    child_idx = 1
                else:
                    child_idx = 2
                split = _insert_rec(node.children[child_idx], key)
                if split:
                    promote, left, right = split
                    node.keys.insert(child_idx, promote)
                    node.children[child_idx] = left
                    node.children.insert(child_idx + 1, right)

            if len(node.keys) > 2:
                return self._split_node(node)
            return None

        split = _insert_rec(self.root, key)
        if split:
            promote, left, right = split
            self.root = Node(keys=[promote], children=[left, right])

    def _split_node(self, node):
        k1, k2, k3 = node.keys
        if node.is_leaf():
            left = Node(keys=[k1])
            right = Node(keys=[k3])
        else:
            c1, c2, c3, c4 = node.children
            left = Node(keys=[k1], children=[c1, c2])
            right = Node(keys=[k3], children=[c3, c4])
        return k2, left, right

    def delete(self, key):
        if self.root is None:
            return


        def _delete_rec(node, key):
            if key in node.keys and node.is_leaf():
                node.keys.remove(key)
            elif key in node.keys:
                idx = node.keys.index(key)
                succ = node.children[idx + 1]
                while not succ.is_leaf():
                    succ = succ.children[0]
                node.keys[idx] = succ.keys[0]
                _delete_rec(succ, succ.keys[0])
            else:
                if node.is_leaf():
                    return
                if key < node.keys[0]:
                    child_idx = 0
                elif len(node.keys) == 1 or key < node.keys[1]:
                    child_idx = 1
                else:
                    child_idx = 2
                _delete_rec(node.children[child_idx], key)

            if node is self.root:
                if len(node.keys) == 0 and node.children:
                    self.root = node.children[0]
                return

            if len(node.keys) >= 1:
                return

            parent, idx = _find_parent(self.root, node)

            left_sib = parent.children[idx - 1] if idx > 0 else None
            right_sib = parent.children[idx + 1] if idx < len(parent.children) - 1 else None

            if left_sib and len(left_sib.keys) == 2:
                borrow_key = left_sib.keys.pop(-1)
                node.keys.insert(0, parent.keys[idx - 1])
                parent.keys[idx - 1] = borrow_key
                if left_sib.children:
                    node.children.insert(0, left_sib.children.pop(-1))
                return
            if right_sib and len(right_sib.keys) == 2:
                borrow_key = right_sib.keys.pop(0)
                node.keys.append(parent.keys[idx])
                parent.keys[idx] = borrow_key
                if right_sib.children:
                    node.children.append(right_sib.children.pop(0))
                return

            if left_sib:
                merge_key = parent.keys.pop(idx - 1)
                left_sib.keys.append(merge_key)
                left_sib.keys += node.keys
                if node.children:
                    left_sib.children += node.children
                parent.children.pop(idx)
            else:
                merge_key = parent.keys.pop(idx)
                node.keys.append(merge_key)
                node.keys += right_sib.keys
                node.children += right_sib.children
                parent.children.pop(idx + 1)

        def _find_parent(curr, target, parent=None):
            if curr is target:
                return parent, None
            if curr.is_leaf():
                return None, None
            for i, c in enumerate(curr.children):
                if c is target:
                    return curr, i
                res = _find_parent(c, target, curr)
                if res[0]:
                    return res
            return None, None

        _delete_rec(self.root, key)
        if self.root and len(self.root.keys) == 0 and self.root.children:
            self.root = self.root.children[0]


    def inorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        if node is None:
            return res
        if node.is_leaf():
            res.extend(node.keys)
        else:
            for i, k in enumerate(node.keys):
                self.inorder(node.children[i], res)
                res.append(k)
            self.inorder(node.children[-1], res)
        return res

    def preorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        if node is None:
            return res
        res.extend(node.keys)
        for c in node.children:
            self.preorder(c, res)
        return res
