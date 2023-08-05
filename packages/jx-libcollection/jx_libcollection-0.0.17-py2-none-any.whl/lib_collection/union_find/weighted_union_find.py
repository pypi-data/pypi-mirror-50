class WeightedUnionFind(object):

    def __init__(self, n):
        self.n = n
        self.parents = range(n)
        self.sizes = [1] * n

    def find(self, p):
        while p != self.parents[p]:
            p = self.parents[p]
        return p

    def is_connected(self, p, q):
        return self.find(p) == self.find(q)

    def __len__(self):
        return self.n

    def union(self, p, q):
        """
        >>> uf = WeightedUnionFind(5)
        >>> uf.parents = [0, 0, 0, 3, 3]
        >>> uf.sizes = [3, 1, 1, 2, 1]
        >>> uf.union(2, 3)
        >>> uf.parents
        [0, 0, 0, 0, 3]
        >>> uf.sizes
        [5, 1, 1, 2, 1]
        """
        p_parent = self.parents[p]
        q_parent = self.parents[q]
        if p_parent == q_parent:
            return

        if self.sizes[p_parent] < self.sizes[q_parent]:
            self.sizes[q_parent] += self.sizes[p_parent]
            self.parents[p_parent] = q_parent
        else:
            self.sizes[p_parent] += self.sizes[q_parent]
            self.parents[q_parent] = p_parent
        self.n -= 1
