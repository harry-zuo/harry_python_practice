"""
输入：s = "  hello world  "
输出："world hello"
解释：反转后的字符串中不能存在前导空格和尾随空格。
"""

s = "a good   example"

def func(s):
    s = s.strip()
    left_p = right_p = len(s) - 1
    answer = []
    while left_p >= 0:
        while left_p >=0 and s[left_p] != " ": left_p -= 1
        answer.append(s[left_p+1:right_p+1])
        while s[left_p] == " ": left_p -= 1
        right_p = left_p

    return " ".join(answer)
        
res = func(s)
print(res)
