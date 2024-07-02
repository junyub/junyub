import sys
n, k = map(int, sys.stdin.readline().split())

num = n
count = 1
def func(n, k):
    lst = []
    global count
    if n % k != 0:
        n = int(str(n) + str(num))
        count += 1
        if n % k in lst:
            print(-1)
            exit()
        else:
            lst.append(n % k)
            func(n, k)
    return count

print(func(n, k))