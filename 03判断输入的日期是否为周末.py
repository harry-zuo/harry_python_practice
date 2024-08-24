# 编写程序，判断今天是否为周末
"""
a = 5
b = [1,2,3,4]
print(a in b) # False
"""

'''
a = "lydia"
b = "i'm lydia"
print(a in b) # True
'''
a = input(f"请输入今天周几:")
b = ["周六","周天","6","7"]
c = a in b

if c == True:
    msg = "今天是周末"
else:
    msg = "今天不是周末"

print(msg)