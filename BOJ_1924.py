x, y = map(int, input().split())

dic = dict(zip([int(m) for m in range(1, 13)], [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]))
cnt = 0

for i in range(1, x):
    cnt += dic[i]

cnt += y
day = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
print(day[cnt%7])