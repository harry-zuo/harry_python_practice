class UionFind:
    def __init__(self, n):
        self.parent = {}
        self.cnt = 0
        for i in range(n):
            self.parent[i] = i
            self.cnt += 1

    def find(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
            return self.parent[x]
        return x

    def union(self, i, j):
        if self.connected(i, j): return
        root_i = self.find(i)
        root_j = self.find(j)
        self.parent[root_i] = self.parent[root_j]
        self.cnt -= 1

    def connected(self, i, j):
        return self.find(i) == self.find(j)


# test
uf = UionFind(1001)
edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]

def func():
    for fr, to in edges:
        if uf.connected(fr, to): return [fr, to]
        uf.union(fr, to)

print(func())
