'''import sys
n, m = map(int, sys.stdin.readline().split())
lst = [0 for _ in range(n)]
for i in range(n):
    lst[i] = list(map(int, sys.stdin.readline().rstrip()))
k = int(sys.stdin.readline())

def func():
    cycle = 0
    while cycle < k:
        cnt = [0 for _ in range(m)]
        for i in lst:
            for j in range(len(i)):
                if i[j] == 0:
                    cnt[j] += 1
        print(f'cnt: {cnt}')
        for i in lst:
            for j in range(len(i)):
                if j == cnt.index(max(cnt)):
                    if i[j] == 0:
                        i[j] = 1
                    else:
                        i[j] = 0
        cycle += 1
    return lst
func()

for i in lst:
    print(i)
result = 0
for i in lst:
    if sum(i) == m:
        result += 1
print(result)'''
#####################################################################
'''import sys
n, m = map(int, sys.stdin.readline().split())
lst = [0 for _ in range(n)]
for i in range(n):
    lst[i] = list(map(int, sys.stdin.readline().rstrip()))
k = int(sys.stdin.readline())

def function(res):
    test = [0 for _ in range(m)]
    for i in res:
        for j in lst:
            if j[i] == 0:
                j[i] = 1
            else:
                j[i] = 0
        for j in lst:
            if sum(j) == m:
                test[i] += 1
        for j in lst:
            if j[i] == 0:
                j[i] = 1
            else:
                j[i] = 0
    return test

def func():
    cycle = 0
    while cycle < k:
        cnt = [0 for _ in range(m)]
        for i in lst:
            for j in range(len(i)):
                if i[j] == 0:
                    cnt[j] += 1
        for i in lst:
            res = []
            for j in range(len(i)):
                if cnt[j] == max(cnt):
                    res.append(j)
        result = function(res)
        for i in result:
            if i == max(result):
                ans = result.index(i)
        for i in lst:
            if i[ans] == 0:
                i[ans] = 1
            else:
                i[ans] = 0
        cycle += 1
    return lst
func()

answer = 0
for i in lst:
    if sum(i) == m:
        answer += 1
print(answer)'''