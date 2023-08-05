class QuickFindUnionFind(object):

    def __init__(self, cnt):
        self.n = cnt
        self.parents = range(cnt)

    def __len__(self):
        """
        >>> uf = QuickFindUnionFind(3)
        >>> len(uf)
        3
        >>> uf.union(1, 2)
        >>> len(uf)
        2
        >>> uf.union(0, 1)
        >>> len(uf)
        1
        >>> uf.parents
        [0, 0, 0]
        """
        return self.n

    def find(self, p):
        """
        >>> uf = QuickFindUnionFind(3)
        >>> uf.find(3)
        Traceback (most recent call last):
            ...
        IndexError: 3
        >>> uf.find(1)
        1
        >>> uf.find(2)
        2
        >>> uf.find(0)
        0
        """
        self._validate(p)
        return self.parents[p]

    def union(self, p, q):
        """
        >>> uf = QuickFindUnionFind(3)
        >>> uf.union(1, 2)
        >>> uf.parents
        [0, 1, 1]
        """
        self._validate(p)
        self._validate(q)
        p_parent = self.find(p)
        q_parent = self.find(q)
        if p_parent == q_parent:
            return
        for i in range(len(self.parents)):
            if self.parents[i] == q_parent:
                self.parents[i] = p_parent
        self.n -= 1

    def is_connected(self, p, q):
        """
        >>> uf = QuickFindUnionFind(3)
        >>> uf.is_connected(0, 1)
        False
        >>> uf.parents[1] = 0
        >>> uf.is_connected(0, 1)
        True
        """
        self._validate(p)
        self._validate(q)
        return self.find(p) == self.find(q)

    def _validate(self, p):
        if not 0 <= p < self.n:
            raise IndexError(p)
