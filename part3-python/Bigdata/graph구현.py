# undirected graph

graph = {'A': set(['B','C']),\
    'B': set(['A','D','E']),\
        'C': set(['A','F']),\
            'D': set(['B']),\
                'E': set(['B','F']),\
                    'F': set(['C','E'])}

def bfs(graph, start):
    visited = [] # 방문 리스트 작성
    queue = [start] # 큐에 스타트 넣어주고

    while queue: # 큐가 빌때까지 돌림
        n = queue.pop(0) # 맨 앞에거 빼고
        if n not in visited: # 뺀게 방문 리스트에 없으면
            visited.append(n) # 리스트에 추가
            print(queue, " 작업 전--")
            queue += graph[n] - set(visited) # 연결된 놈 큐에 넣어주고 방문리스트에 있으면 제외
            print(queue, " 작업 후--")
    return visited

a = bfs(graph,'A')
print(a)

def bfs_paths(graph, start, goal):
    queue = [(start,[start])]
    result = []

    while queue:
        n, path = queue.pop(0)
        if n == goal:
            result.append(path)
        else:
            for m in graph[n] - set(path):
                print(queue, " 작업 전--")
                queue.append((m, path+[m]))
                print(queue, " 작업 후--")
    return result

b = bfs_paths(graph, 'A', 'F')
print(b)