#a = 4 >= 5 or 3 > 1 and 10 / 2 == 5
#print(a)

"""
a = input("请输入一个数字：")
print(f"a 的值为:{a}, a 的类型为:{type(a)}")
a = int(a)
print("开始转换类型")
print(f"a 的值为:{a}, a 的类型为:{type(a)}")
"""

a =0
while a <= 9:
    a += 1
    if a == 5:
        continue
    print(a)
print("循环结束")

n = int(input(f"请输入一个数字:"))



for b in range(1, n):
    n -= 1
    if n ==5:
        continue
    print(n)

## TODO 用 for 循环实现上述 while 同样的结果，完成后提交 pr 并告知