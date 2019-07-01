INF = 100000000

graph = [[0, 2, 5, 1,INF,INF],
         [2, 0, 3, 2,INF,INF],
         [5, 3, 0, 3,  1,  5],
         [1, 2, 3, 0, 1, INF],
         [INF, INF, 1,1,0, 2],
         [INF,INF,5, INF,2,0]]

SIZE = len(graph[0])

visited = set()
distance = []
# print(distance)

def getSmallIndex():
    global graph, distance, visited, SIZE
    min = INF
    index = 0
    for i in range(SIZE):
        # print(visited)
        if distance[i] < min and i not in visited:
            min = distance[i]
            index = i
    # print(distance)
    # print(index)
    return index # 가장 distance 짧은 node번호 리턴

def dajikstra(start):
    global graph, distance, visited, SIZE
    distance = graph[start][:]
    visited.add(start)
    # print("dsf")
    # print(visited)
    for _ in range(SIZE):
        node = getSmallIndex()
        visited.add(node)
        # print(visited)
        for k in range(SIZE):
            if k not in visited:
                if distance[k] > distance[node]+ graph[node][k]:
                    distance[k] = distance[node] + graph[node][k]

    return distance

print(dajikstra(0))
print(distance)