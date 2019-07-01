# 현재 이 함수는 큰 값일수록 위에, 

class Node(object): # node object 만들어 주고
    def __init__(self,data):
        self.data = data # 자기값
        self.left = self.right = None # 자기 밑 left right는 None이 기본값

class BinarySearchTree(object): # binary search를 위한 class 생성
    def __init__(self): # 맨 처음 root는 None
        self.root = None

    # 이제 여기에 원소를 추가, 삭제, 탐색할 수 있도록 insert / delete / find 메서드를 추가해야 함

    def insert(self, data):
        self.root = self._insert_value(self.root, data) # 현재 트리의 루트에 _insert_value의 값 대입
        return self.root is not None # self.root가 None이면 False, None 아니면 True : 트리가 비어있는지 아닌지 확인용

    def _insert_value(self, node, data): # 재귀적으로 돌림
        if node is None: # node는 맨처음 비어있움, 결국 빈 곳이 보이면 넣어줌
            node = Node(data) # node에 Node 객체 넣어줌
        else:
            if data <= node.data:
                node.left = self._insert_value(node.left, data) # _insert_value의 첫번째 인자(node)가 None이 되어 결정될 때까지 재귀
            else:
                node.right = self._insert_value(node.right, data)
        return node

    def find(self, key):
        return self._find_value(self.root, key) # 아 이거 있는가 없는가 나타내는 함수 : 트리안에 인자가 있으면 True, 없으면 False

    def _find_value(self, root, key):
        if root is None or root.data == key:
            return root is not None # root(라고 써있지만 결국 찾아간 노드)가 None이 아니면(root.data==key) True, 반대는(root is None) False
        elif key < root.data:
            return  self._find_value(root.left, key) # None 또는 key 나올 때 까지 재귀호출
        else:
            return  self._find_value(root.right, key)

    def delete(self, key):
        self.root, deleted = self._delete_value(self.root, key)
        return deleted

    def _delete_value(self, node, key):
        if node is None: # 탐색해서 계속 파고들어갔는데 결국 None이면
            return node, False 

        deleted = False # 탐색한 node가 일단 None이 아니면(값이 있으면)
        if key == node.data: # 현재 노드가 찾던 데이터면 # 참고 : 노드는 안변함
            deleted = True # deleted 값을 True로 바꾸고 : 현재 노드 지울꺼임
            if node.left and node.right: # 노드 양쪽이 꽉 차있으면
                parent, child = node, node.right # 부모(삭제예정), 자식(부모가 될)
                print(parent.data,"1111111111111")
                while child.left is not None:
                    parent, child = child, child.left # 오른쪽놈을 왼쪽 끝까지 파고들어서
                    print(parent.data,"32423324322")
                child.left = node.left # 오른쪽놈의 왼쪽 끝에 왼쪽놈 갖다붙여줌
                print(parent.data,"dsflsdln")
                if parent != node: # 전단계에서 왼쪽놈들 오른쪽에 왼쪽에 붙이려고 parent랑 child가 바뀐거 정리해줌
                    print(parent.left.data,"3rwef")
                    parent.left = child.right # child보다 큰놈들 싹 붙이고 : 이렇게 덮어씌운다고 child 자체의 data가 사라지지 않음!
                    # print(parent.left,"3rwef3223")
                    print(child.data)
                    child.right = node.right # node.right가 parent이거나 parent +  어쨌든 child보다 큰놈들 총집합
                    # 즉 목적 : child를 기준으로 정렬
                node = child
            elif node.left:
                node = node.left
            elif node.right:
                node = node.right
            else:
                node = None
        elif key < node.data:
            node.left, deleted = self._delete_value(node.left, key)
        else:
            node.right, deleted = self._delete_value(node.right, key)
        return node, deleted


bts = BinarySearchTree()
array = [11,8,1,9,15,13,17,16,19,14]
for x in array:
    bts.insert(x)

bts.delete(15)

# print(bts.root.right.left.left)
print(bts.root.right.left.data)
print(bts.root.right.data)

print(bts.find(15))



