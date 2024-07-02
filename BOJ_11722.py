n = int(input())
graph = [int(x) for x in input().split()]
dp = [1 for _ in range(n)]

for i in range(n):
    for j in range(i):
        if graph[j] > graph[i]:
            dp[i] = max(dp[i], dp[j]+1)

print(max(dp))


1, 2, 3, 5, 8, 13