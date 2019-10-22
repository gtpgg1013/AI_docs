# 이 문제는 출력때문에 ㅈㄴ 고민한 ㅄ같은 문제였다
# 이 김에 그냥 Queue를 구현해보자.
# 시간초과 뜬다. 그냥 잘 구현된 라이브러리를 쓰자.

import collections
import sys

class Queue:
    def __init__(self,arr):
        self.arr = arr
    def append(self,arg):
        # print(self.arr)
        # print(arg)
        # print(self.arr.append(arg))
        self.arr += str(arg)
        # print(self.arr, 'wow')
    def isEmpty(self):
        if len(self.arr):
            return False
        else:
            return True
    def popleft(self):
        # print(self.arr, 'ho')
        val = self.arr[0]
        # print(val)
        # print(self.arr[1:])
        self.arr = self.arr[1:]
        # print(self.arr,' ayay')
        return val

inp = sys.stdin.readline().strip().split(' ')
N = int(inp[0])
K = int(inp[1])

queue = Queue([i+1 for i in range(N)])
#queue = collections.deque([i+1 for i in range(N)])
output_str = '<'

# print(queue.arr)
while True:
    for k in range(K-1):
        tmp = queue.popleft()
        queue.append(tmp)
    tmp = queue.popleft()
    # print(tmp, 'here')
    if queue.isEmpty():
        output_str += str(tmp) + ">"
        break
    else:
        output_str += str(tmp) + ", "

print(output_str)