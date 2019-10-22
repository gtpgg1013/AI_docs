import collections
import sys

inp = sys.stdin.readline().strip().split(' ')
N = int(inp[0])
K = int(inp[1])

queue = collections.deque([i+1 for i in range(N)])
output_str = '<'

while True:
    for k in range(K-1):
        tmp = queue.popleft()
        queue.append(tmp)
    tmp = queue.popleft()
    if not len(queue):
        output_str += str(tmp) + ">"
        break
    else:
        output_str += str(tmp) + ", "

print(output_str)