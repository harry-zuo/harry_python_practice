""" algorithm
输入：height = [0,1,0,2,1,0,1,3,2,1,2,1]
输出：6
"""

height = [0,1,0,2,1,0,1,3,2,1,2,1]

left_wall = 0
right_wall = 0
result = 0

for i in range(len(height) - 1):
    left_wall = max(left_wall, height[i])
    if left_wall == 0:
        continue
    right_wall = max(right_wall, height[i + 1])
    if right_wall == 0:
        continue
    result += min(left_wall, right_wall)
    left_wall, right_wall = right_wall, 0

print(result)
