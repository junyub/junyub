import sys
country = sys.stdin.readline().split()
score = [0 for x in range(4)]

for i in range(6):
    a, b, w, d, l = sys.stdin.readline().split()
    if float(w) >= float(d) + float(l):
        score[country.index(a)] += 3
    elif float(l) >= float(d) + float(w):
        score[country.index(b)] += 3
    else:
        score[country.index(a)] += 1
        score[country.index(b)] += 1

ans = [0 for x in range(4)]
max = max(score)
min = min(score)
mid = sum(score) - max - min
for i in range(4):
    if score[i] == max:
        ans[i] = score[i] / max
    elif score[i] == min:
        if min == 0:
            ans[i] = score[i]
        else:
            ans[i] = score[i] / min
    else:
        ans[i] = score[i] / mid

for i in ans:
    print(f'{i:.10f}')