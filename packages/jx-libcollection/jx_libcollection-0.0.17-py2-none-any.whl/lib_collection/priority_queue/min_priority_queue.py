class MinPriorityQueue(object):
    def __init__(self):
        self.keys = [None] * 2
        self.n = 0

    def __len__(self):
        """
        >>> q = MinPriorityQueue()
        >>> len(q)
        0
        >>> q.push(3)
        >>> q.push(2)
        >>> q.push(1)
        >>> len(q)
        3
        >>> q.pop()
        1
        >>> len(q)
        2
        """
        return self.n

    def push(self, v):
        """
        >>> q = MinPriorityQueue()
        >>> q.push(3)
        >>> q.min
        3
        >>> q.push(2)
        >>> q.min
        2
        >>> q.push(1)
        >>> q.min
        1
        """
        if self.n + 1 == len(self.keys):
            self._resize(2*len(self.keys))

        self.n += 1
        self.keys[self.n] = v
        self._swim(self.n)

    def pop(self):
        """
        >>> q = MinPriorityQueue()
        >>> q.push(1)
        >>> q.push(3)
        >>> q.push(2)
        >>> q.pop()
        1
        >>> q.keys
        [None, 2, 3, None]
        >>> q.pop()
        2
        >>> q.pop()
        3
        >>> q.pop()
        Traceback (most recent call last):
            ...
        IndexError: underflow
        """
        if not self.n:
            raise IndexError('underflow')

        keys = self.keys
        res = keys[1]
        keys[1], keys[self.n] = keys[self.n], keys[1]
        keys[self.n] = None
        self.n -= 1

        self._sink(1)

        if self.n and self.n * 4 == len(self.keys)-1:
            self._resize(len(self.keys)/2)
        return res

    @property
    def min(self):
        """
        >>> q = MinPriorityQueue()
        >>> q.min
        Traceback (most recent call last):
            ...
        IndexError: underflow
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 4, 1, 2]
        >>> q.n = 3
        >>> q.min
        4
        """
        if not self.n:
            raise IndexError('underflow')
        return self.keys[1]

    def _swim(self, n):
        """
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 2, 3, None, 1]
        >>> q.n = 4
        >>> q._swim(4)
        >>> q.keys
        [None, 1, 2, None, 3]
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 3, 2, None, 1]
        >>> q.n = 4
        >>> q._swim(4)
        >>> q.keys
        [None, 1, 3, None, 2]
        """
        keys = self.keys
        while n > 1 and keys[n/2] > keys[n]:
            keys[n/2], keys[n] = keys[n], keys[n/2]
            n /= 2

    def _sink(self, n):
        """
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 3, 2, 1]
        >>> q.n = 3
        >>> q._sink(1)
        >>> q.keys
        [None, 1, 2, 3]
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 3, 1, 2]
        >>> q.n = 3
        >>> q._sink(1)
        >>> q.keys
        [None, 1, 3, 2]
        """
        keys = self.keys
        while 2 * n <= self.n:
            i = 2 * n
            if i < self.n and keys[i+1] < keys[i]:
                i += 1

            if keys[i] >= keys[n]:
                break

            keys[i], keys[n] = keys[n], keys[i]
            n = i

    def _resize(self, n):
        """
        >>> q = MinPriorityQueue()
        >>> q.keys = [None, 1, 2, 3]
        >>> q.n = 3
        >>> q._resize(6)
        >>> q.keys
        [None, 1, 2, 3, None, None]
        """
        tmp = [None]*n
        for i in range(self.n+1):
            tmp[i] = self.keys[i]
        self.keys = tmp
