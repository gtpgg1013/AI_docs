class Node(object):
    def __init__(self, data):
        self.data = data
        self.right = self.left = None

# root는 Node, data는 숫자
class BinarySearchTree2(object):
    def __init__(self):
        self.root = None

    def insert(self, data):
        self.root = self._insert_value(self.root, data)
        return self.root is not None

    def _insert_value(self, node, data):
        if node is None:
            self.root = Node(data)
        else:
            if data <= node.data:
                self.root = self._insert_value(node.left, data)
            else:
                self.root = self._insert_value(node.right, data)
        return node

    def find(self, data):
        return self._find_value(self.root, data)

    def _find_value(self, node, data):
        if node is None:
            return False
        elif node.data == data:
            return True
        else:
            if data <= node.data:
                self._find_value(node.left, data)
            else:
                self._find_value(node.right, data)

    def delete(self, data):
        self.root, deleted = self._delete_value(self.root, data)
        return deleted

    def _delete_value(self, node, data):
        if node is None: # 없으면
            return node, False

        deleted = False
        if data == node.data:
            deleted = True
            if node.left and node.right:
                parent, chlid = node, node.right
                while child.left is not None: # 오른쪽 가장 작은 놈 왼쪽에 node.left 붙이기
                    parent, child = child, child.left
                child.left = node.left
                if parent != node:
                    parent.left = child.left
                    child.right = node.right
                node = child
            elif node.left: # 왼쪽만 있긔
                node = node.left
            elif node.right: # 오른쪽만 있긔
                node = node.right
            else: # 양쪽 다 없귀
                node = None
        elif data < node.data:
            node.left, deleted = self._delete_value(node.left, data)
        else:
            node.right, deleted = self._delete_value(node.right, data)
        return node, deleted


