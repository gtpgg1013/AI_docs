graph = {'A': ['B','C'],\
    'B': ['A','D','E'],\
        'C': ['A','F'],\
            'D': ['B'],\
                'E': ['B','F'],\
                    'F': ['C','E']}

def bfs(graph,start):
    visited = []
    queue = [start]

    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.append(node)
        for nxtnode in graph[node]:
            print(queue)
            if nxtnode not in visited:
                queue.append(nxtnode)
    return visited

res = bfs(graph, 'A')
print(res)

