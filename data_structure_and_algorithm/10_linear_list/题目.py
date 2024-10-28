"""
1. 两数之和
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。
你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。
你可以按任意顺序返回答案。

示例 1：

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：

输入：nums = [3,2,4], target = 6
输出：[1,2]
示例 3：

输入：nums = [3,3], target = 6
输出：[0,1]
示例 4：

输入：nums = [3,2,3], target = 6
输出：[0,2]

提示：

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
只会存在一个有效答案

标签：数组 哈希表

# class Solution:
#     def twoSum(self, nums: list[int], target: int) -> list[int]:
#         # O(n^2)  1350 ms
#         for l in range(len(nums)-1):
#             for r in range(l+1, len(nums)):
#                 if nums[l] + nums[r] == target:
#                     return l, r
                
#         # O(n)  4ms
#         # 和上述暴力的解法相比，哈希的优势就是 用 O(1) 的时间找到 O(n) 的解，因此 T(O) 优化结果: n^2 --> n 
#         r_idx = {}
#         for l_idx, num in enumerate(nums):
#             if target - num in r_idx:
#                 return l_idx, r_idx[target - num]
#             r_idx[num] = l_idx

"""


"""
49. 字母异位词分组
给你一个字符串数组，请你将 字母异位词 组合在一起。可以按任意顺序返回结果列表。
字母异位词 是由重新排列源单词的所有字母得到的一个新单词。
 

示例 1:

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
输出: [["bat"],["nat","tan"],["ate","eat","tea"]]
示例 2:

输入: strs = [""]
输出: [[""]]
示例 3:

输入: strs = ["a"]
输出: [["a"]]
 

提示：

1 <= strs.length <= 104
0 <= strs[i].length <= 100
strs[i] 仅包含小写字母

标签： 数组 哈希表 字符串 排序

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # O(n)
        d = defaultdict(list)
        for string in strs:
            sorted_string = "".join(sorted(string))
            d[sorted_string].append(string)
        return list(d.values())

"""


"""
128. 最长连续序列
给定一个未排序的整数数组 nums ，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。
请你设计并实现时间复杂度为 O(n) 的算法解决此问题。


示例 1：

输入：nums = [100,4,200,1,3,2]
输出：4
解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。
示例 2：

输入：nums = [0,3,7,2,5,8,4,6,0,1]
输出：9
 

提示：

0 <= nums.length <= 105
-109 <= nums[i] <= 109

标签：并查集 数组 哈希表

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        # O(nlgn)
        # nums = sorted(set(nums))
        # cnt = max_cnt = 1
        # for i in range(1,len(nums)):
        #     if nums[i-1] + 1 == nums[i]:
        #         cnt += 1
        #     else:
        #         cnt = 1
        #     max_cnt = max(max_cnt, cnt)
        # return max_cnt if len(nums) else 0


        # O(n)
        # Hashtable
        # d = {}
        # res = 0
        # for num in nums:
        #     if num not in d:
        #         left = d[num - 1] if num - 1 in d else 0
        #         right = d[num + 1] if num + 1 in d else 0
        #         length = left + right + 1
        #         d[num] = d[num - left] = d[num + right] = length
        #         res = max(res, length)
        # return res

        # O(n) 并查集
        # nums = set(nums)
        # ans = 0
        # uf = {num: num for num in nums}
        # size = {num: 1 for num in nums}

        # def find(x):
        #     if uf[x] != x:
        #         uf[x] = find(uf[x])
        #     return uf[x]

        # def union(fr, to):
        #     root_fr = find(fr)
        #     root_to = find(to)
        #     if root_fr != root_to:
        #         uf[root_fr] = root_to
        #         size[root_to] += size[root_fr]

        # for num in nums:
        #     if num + 1 in uf:
        #         union(num, num + 1)
        # if size:
        #     ans = max(size.values())
        # return ans

"""


"""
283. 移动零
给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
请注意 ，必须在不复制数组的情况下原地对数组进行操作。

 
示例 1:

输入: nums = [0,1,0,3,12]
输出: [1,3,12,0,0]
示例 2:

输入: nums = [0]
输出: [0]

提示:

1 <= nums.length <= 104
-231 <= nums[i] <= 231 - 1
 
标签： 数组 双指针

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        
        # 记零值的偏移量，遇到非零则左移偏移量 O(n)
        # offset = 0
        # for idx in range(len(nums)):
        #     if nums[idx] == 0:
        #         offset += 1
        #     elif offset:
        #         nums[idx - offset], nums[idx] = nums[idx], 0

        # 双指针 O(n)
        l = 0
        for r in range(len(nums)):
            if nums[r] != 0:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
                
"""


# def func():
#     pass
#     return
        
# res = func()
# print(res)