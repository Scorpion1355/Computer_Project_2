""" Tree Factory """

from tree_adapters import (
    AVLTreeAdapter,
    RedBlackTreeAdapter,
    SplayTreeAdapter,
    BTreeAdapter,
    TwoThreeTreeAdapter
)

class TreeFactory:

    @staticmethod
    def create_tree(tree_type):

        tree_type = tree_type.lower()

        if tree_type == "avl":
            return AVLTreeAdapter()
        if tree_type == "red-black":
            return RedBlackTreeAdapter()
        if tree_type == "splay":
            return SplayTreeAdapter()
        if tree_type == "b-tree":
            return BTreeAdapter(3)
        if tree_type == "2-3-tree":
            return TwoThreeTreeAdapter()
        raise ValueError(f"Unknown tree type: {tree_type}")
