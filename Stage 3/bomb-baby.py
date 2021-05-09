def solution(x, y):
    x, y = int(x), int(y)
    if x == y:
        return "impossible"
    if x > y:
        x, y = y, x
    count = 0
    while True:
        if x == 0:
            return "impossible"
        if x == 1:
            count += y - 1
            return str(count)
        count += y // x
        x, y = y % x, x



