""" abstract class """

from abc import ABC, abstractmethod

class SelfBalancingTree(ABC):
    @abstractmethod
    def insert(self, key):

        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def search(self, key):
        pass

    @abstractmethod
    def inorder_traversal(self):
        pass

    @abstractmethod
    def preorder_traversal(self):
        pass

    def is_empty(self):
        return True