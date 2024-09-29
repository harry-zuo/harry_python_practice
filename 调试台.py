"""
输入：tickets = [2,3,2], k = 2

输出：6
"""

tickets = [2,3,2]
k = 2

def func():
    i = ans = 0
    while tickets[k] > 0:
        if tickets[i] > 0:
            tickets[i] -= 1
            ans += 1
        i += 1
        if i == len(tickets):
            i = 0
    return ans
        

res = func()
print(res)
