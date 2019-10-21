inp = input().split(' ')
N = int(inp[0])
K = int(inp[1])

li = [1 for _ in range(N)]
idx = -1
res = []

for _ in range(N):
    tmp = K
    while True:
        if idx < N-1:
            idx += 1
        else:
            idx = 0
        if li[idx]==1:
            tmp -= 1
        if tmp==0:
            li[idx] = 0
            res.append(int(idx)+1)
            break

print(res)