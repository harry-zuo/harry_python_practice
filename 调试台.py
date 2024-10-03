"""
输入：dist = [1,3,2], hour = 1.9
输出：-1

输入：dist = [1,3,2], hour = 2.7
输出：3
"""

dist = [1,3,2]
hour = 6

def func(dist: list[int], hour: float) -> int:
    n = len(dist)
    h100 = round(hour * 100)
    delta = h100 - (n - 1) * 100
    if delta <= 0:
        return -1

    max_dist = max(dist)
    if n * 100 >= h100:
        return max(max_dist, (dist[-1]*100 - 1)//delta + 1)

    def check(v: int) -> bool:
        t = n - 1
        for d in dist[:-1]:
            t += d - 1 // v
        return (t * v + dist[-1]) * 100 <= h100 * v

    left = 0
    h = h100 // (n * 100)
    right = (max_dist - 1) // h + 1
    while left + 1 < right:
        mid = (left + right) // 2
        if check(mid):
            right = mid
        else:
            left = mid
    return right
        
    return speed
        
res = func(dist, hour)
print(res)


