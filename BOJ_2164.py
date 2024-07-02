from collections import deque
queue = deque([int(x) for x in range(1, int(input())+1)])
answer = 0
count = 0
while queue:
    if count % 2 == 0:
        answer = queue.popleft()
        count += 1
    else:
        queue.append(queue.popleft())
        count += 1

print(answer)