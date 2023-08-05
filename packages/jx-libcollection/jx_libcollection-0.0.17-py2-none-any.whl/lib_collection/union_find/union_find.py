class UnionFind(object):

    def __init__(self, n):
        self.n = n
        self.parents = range(n)
        self.ranks = [0] * n

    def find(self, p):
        """
        >>> uf = UnionFind(5)
        >>> uf.parents = [0, 1, 2, 2, 3]
        >>> uf.find(4)
        2
        >>> uf.parents
        [0, 1, 2, 2, 2]
        """
        while p != self.parents[p]:
            self.parents[p] = self.parents[self.parents[p]]
            p = self.parents[p]
        return p

    def is_connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        """
        >>> uf = UnionFind(5)
        >>> uf.parents = [0, 1, 2, 3, 3]
        >>> uf.union(3, 4)
        >>> uf.parents
        [0, 1, 2, 3, 3]
        >>> uf = UnionFind(5)
        >>> uf.parents = [0, 0, 0, 3, 3]
        >>> uf.ranks = [1, 0, 0, 1, 0]
        >>> uf.union(2, 3)
        >>> uf.parents
        [0, 0, 0, 0, 3]
        >>> uf.ranks
        [2, 0, 0, 1, 0]
        """
        p_parent = self.parents[p]
        q_parent = self.parents[q]
        if p_parent == q_parent:
            return

        if self.ranks[p_parent] < self.ranks[q_parent]:
            self.parents[p_parent] = q_parent
        elif self.ranks[p_parent] > self.ranks[q_parent]:
            self.parents[q_parent] = p_parent
        else:
            self.parents[q_parent] = p_parent
            self.ranks[p_parent] += 1
        self.n -= 1
