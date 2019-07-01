class Node(object): # node object 만들어 주고
    def __init__(self,data):
        self.data = data
        self.left = self.right = None

class BinarySearchTree(object): # binary search를 위한 class 생성
    def __init__(self): # 맨 처음 root는 None
        self.root = None

    # 이제 여기에 원소를 추가, 삭제, 탐색할 수 있도록 insert / delete / find 메서드를 추가해야 함

    def insert(self, data):
        self.root = self._insert_value(self.root, data)
        return self.root is not None # self.root가 None이면 False, None 아니면 True

    def _insert_value(self, node, data): # 재귀적으로 돌림
        if node is None: # node는 맨처음 비어있움
            node = Node(data) # node에 Node 객체 넣어줌
        else:
            if data <= node.data:
                node.left = self._insert_value(node.left, data)
            else:
                node.right = self._insert_value(node.right, data)
        return node

    def find(self, key):
        return self._find_value(self.root, key)

    def _find_value(self, root, key):
        if root is None or root.data == key:
            return root is not None
        elif key < root.data:
            return  self._find_value(root.left, key)
        else:
            return  self._find_value(root.right, key)

    def delete(self, key):
        self.root, deleted = self._delete_value(self.root, key)
        return deleted

    def _delete_value(self, node, key):
        if node is None:
            return node, False

        deleted = False
        if key == node.data:
            deleted = True
            if node.left and node.right: # 노드 양쪽이 꽉 차있으면
                parent, child = node, node.right:



