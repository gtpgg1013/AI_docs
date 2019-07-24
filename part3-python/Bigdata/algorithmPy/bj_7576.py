from collections import deque

class xy:
    def __init__(self,x,y,count):
        self.x = x
        self.y = y
        self.count = count

txys = [(0,1),(1,0),(-1,0),(0,-1)]

num = input().split(" ")
M = int(num[0])
N = int(num[1])

rescnt = 0

box = []
visited = []
queue = deque()
for _ in range(N):
    tmp = input().split(" ")
    tmp = list(map(int, tmp))
    box.append(tmp)

for _ in range(N):
    tmp = []
    for _ in range(M):
        tmp.append(False)
    visited.append(tmp)

for i in range(N):
    for k in range(M):
        if box[i][k]==1:
            queue.append(xy(k,i,0))
            visited[i][k] = True
        if box[i][k]==-1:
            visited[i][k] = True

if len(queue)==M*N:
    res = 0
else:
    while(len(queue)!=0):
        # print("--")
        head = queue.popleft()
        x = head.x
        y = head.y
        count = head.count
        # print(x, y,count)
        for txy in txys:
            tmpx = x + txy[0]
            tmpy = y + txy[1]
            # print(txy)
            # print(tmpx,tmpy)
            if tmpx >= 0 and tmpx < M and tmpy >= 0 and tmpy < N:
                if visited[tmpy][tmpx] == False:
                    visited[tmpy][tmpx] = True
                    queue.append(xy(tmpx,tmpy,count+1))
                    # print(x, y)
                    if count+1 > rescnt:
                        rescnt = count + 1
    flag = False
    for i in range(N):
        for k in range(M):
            if visited[i][k] == False:
                flag = True
                break
        if flag == True:
            break

    if flag == True:
        res = -1
    else:
        res = rescnt


# print(box)
# print(visited)
# print(queue[0].x)
# print(queue[0].y)

print(res)