from collections import deque

m, n = map(int, input().split())
graph = []
for _ in range(m):
    graph.append(list(map(int, input().rstrip())))

visited = [[0 for _ in range(n)] for _ in range(m)]
queue = deque()
for i in range(n):
    if graph[0][i] == 0:
        visited[0][i] = 1
        queue.append((0, i))

dx = [-1, 1, 0 ,0]; dy = [0, 0, -1, 1]
while queue:
    x, y = queue.popleft()
    if x == m-1:
        print('YES')
        exit()
    for i in range(4):
        nx = x + dx[i]; ny = y + dy[i]
        if 0 <= nx < m and 0 <= ny < n and visited[nx][ny] == 0 and graph[nx][ny] == 0:
            visited[nx][ny] = 1
            queue.appendleft((nx, ny))

print('NO')