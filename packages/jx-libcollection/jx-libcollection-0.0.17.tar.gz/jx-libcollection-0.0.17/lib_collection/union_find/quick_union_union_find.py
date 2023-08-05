class QuickUnionUnionFind(object):

    def __init__(self, n):
        self.n = n
        self.parents = range(n)

    def __len__(self):
        return self.n

    def union(self, p, q):
        """
        >>> uf = QuickUnionUnionFind(5)
        >>> uf.parents = [0, 1, 1, 2, 4]
        >>> uf.union(1, 3)
        >>> uf.parents
        [0, 1, 1, 2, 4]
        >>> uf.union(1, 4)
        >>> uf.parents
        [0, 1, 1, 2, 1]
        """
        p_parent = self.find(p)
        q_parent = self.find(q)
        if p_parent == q_parent:
            return
        self.parents[q] = p_parent
        self.n -= 1

    def find(self, p):
        """
        >>> uf = QuickUnionUnionFind(3)
        >>> uf.find(1)
        1
        >>> uf = QuickUnionUnionFind(5)
        >>> uf.parents = [0, 1, 1, 2, 4]
        >>> uf.find(3)
        1
        """
        while p != self.parents[p]:
            p = self.parents[p]
        return p

    def is_connected(self, p, q):
        """
        >>> uf = QuickUnionUnionFind(5)
        >>> uf.parents = [0, 1, 1, 2, 4]
        >>> uf.is_connected(1, 3)
        True
        >>> uf.is_connected(1, 4)
        False
        """
        return self.find(p) == self.find(q)
