import collections
import sys

inp = sys.stdin.readline().strip().split(' ')
N = int(inp[0])
K = int(inp[1])

queue = collections.deque([i+1 for i in range(N)])
res = []

for _ in range(N):
    for i in range(K):
        if i != K-1:
            tmp = queue.popleft()
            queue.append(tmp)
        else: 
            res.append(queue.popleft())

print('<',end='')
for i in range(len(res)-1):
    print(res[i],end=',')
print(res[-1],end=">")