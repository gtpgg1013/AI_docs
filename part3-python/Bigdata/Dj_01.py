# 무한대 숫자 표현
INF = 100000000

# 2차원 배열로 그래프 표현
graph = [[0, 2, 5, 1,INF,INF],
         [2, 0, 3, 2,INF,INF],
         [5, 3, 0, 3,  1,  5],
         [1, 2, 3, 0, 1, INF],
         [INF, INF, 1,1,0, 2],
         [INF,INF,5, INF,2,0]]

# 거리값 저장할 배열
distance = []

# 방문한 노드를 저장할 set 자료구조
visited = set()

# graph의 사이즈(어짜피 정방형이니까)
SIZE = len(graph[0])

def getSmallIndex():
    global graph, distance, visited, INF, SIZE
    min = INF # min을 최댓값으로 잡고
    index = 0 # 인덱스 0 잡아주고
    for i in range(SIZE): # 다른 모든 노드와 비교
        if min > distance[i] and i not in visited: # 가장 작은 값이면서 방문하지 않은 노드
            min = distance[i]
            index = i
    return index # 찾기

def dajikstra(start):
    global graph, distance, visited, INF, SIZE
    distance = graph[start][:] # 초기값 배열
    visited.add(start) # 맨 처음 시작할 노드 visit에 추가
    for _ in range(SIZE): # 6번 돌려
        current = getSmallIndex() # 현재 상태에서 가장 짧은 값 찾기
        visited.add(current) # 그놈 인덱스 visit에 넣고
        for k in range(SIZE): # 다른 노드들과 다 비교
            # 그리고 distance 배열에 있는 값과 새로운 값과 비교해서 작은 값으로 갱신
            if k not in visited and distance[k] > distance[current] + graph[current][k]:
                distance[k] = distance[current] + graph[current][k]

dajikstra(3)
print(distance)
