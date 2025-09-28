x = int(input(f"请输入一个数字:"))
def print_square(side_length, char='*'):
    if not isinstance(side_length, int) or side_length <= 0:
        print("请输入正整数作为边长")
        return
    
    # 打印正方形
    for i in range(side_length):
        # 每一行打印side_length个字符
        print(char * side_length)
    return
print_square(x)