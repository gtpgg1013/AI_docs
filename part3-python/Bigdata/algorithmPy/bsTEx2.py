class Node(object):
    def __init__(self,data):
        self.data = data
        self.right = self.left = None

class BinarySearchTree3(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert_value(self.root, data)
        return self.root is not None

    def _insert_value(self, node, data):
        if node is None:
            node = Node(data)
        else:
            if data >= node.data:
                self.root = self._insert_value(node.right,data)
            else:
                self.root= self._insert_value(node.left, data)
        return node

    def find(self, data):
        return self._find_value(self.root, data)

    def _find_value(self, node, data):
        if node is None or node.data == data:
            return node is not None # None이면 False, 아니면 True
        else:
            if data >= node.data:
                return self._find_value(node.right, data)
            else:
                return self._find_value(node.left, data)

    def delete(self, data):
        self.root, deleted = self._delete_value(self.root, data)
        return deleted

    def _delete_value(self, node, data):
        if node is None:
            return node, False

        deleted = False
        if data == node.data:
            deleted = True
            if node.left and node.right:
                parent, child = node, node.right
                while child.left is not None:
                    parent, chile = child, child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.right
                    child.right = node.rihgt
                node = child
            elif node.left:
                node = node.left
            elif node.right:
                node = node.right
            else:
                node = None
        elif data < node.data:
            node.left, deleted = self._delete_value(node.left, data)
        else:
            node.right, deleted = self._delete_value(node.right, data)
        return node, deleted
