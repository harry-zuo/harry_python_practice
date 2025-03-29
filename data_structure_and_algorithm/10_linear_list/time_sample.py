cur_version = '3.6' # 4 6
new_version = '3.6.11' # 3 11
# 大版本.小版本.子版本 发型号

# 入门版的版本比较算法，约定好格式 大版本.小版本.子版本
def compare_version(cur_version, new_version):
    cur_parts = list(map(int, cur_version.split('.')))
    new_parts = list(map(int, new_version.split('.')))

    # 遍历每个版本号部分进行比较
    for cur, new in zip(cur_parts, new_parts):
        if cur > new:
            return '不做处理'
        elif cur < new:
            return '去升级'
    # 如果前面的部分都相同，检查新版本号是否有更多部分
    if len(new_parts) > len(cur_parts):
        return '去升级'
    return '不做处理'

res = compare_version(cur_version, new_version)
print(res)

""" # Solution 2
继续后续比较
去升级 或 不用做任何处理
"""

""" # Solution 1
去升级
cv loop 后续逻辑
nv loop 后续逻辑
去升级
cv loop 后续逻辑
"""

""" 不加任何中断的结果
不用做任何处理
nv loop 后续逻辑
nv loop 后续逻辑
cv loop 后续逻辑
nv loop 后续逻辑
去升级
nv loop 后续逻辑
cv loop 后续逻辑
"""


