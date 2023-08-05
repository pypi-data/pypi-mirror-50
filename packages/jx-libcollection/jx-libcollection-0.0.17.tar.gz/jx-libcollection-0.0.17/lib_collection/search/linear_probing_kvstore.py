class LinearProbingKVStore(object):

    def __init__(self, d=None, capacity=4):
        """
        >>> d = LinearProbingKVStore({'a': 1, 'b': 2})
        >>> d['a']
        1
        >>> d['b']
        2
        """
        self.capacity = capacity
        self.n = 0
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

        if d:
            s = LinearProbingKVStore(capacity=capacity)
            for k, v in d.items():
                s[k] = v
            self.n = s.n
            self.keys = s.keys
            self.values = s.values

    def __repr__(self):
        """
        >>> d = LinearProbingKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> d
        LinearProbingKVStore({'a': 1, 'b': 2})
        """
        s = ', '.join('{}: {}'.format(repr(k), repr(v)) for k, v in self.items())
        return 'LinearProbingKVStore({%s})' % s

    def __len__(self):
        """
        >>> d = LinearProbingKVStore()
        >>> len(d)
        0
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> len(d)
        2
        >>> del d['a']
        >>> len(d)
        1
        """
        return self.n

    def __contains__(self, k):
        """
        >>> d = LinearProbingKVStore()
        >>> 'a' in d
        False
        >>> d['a'] = 1
        >>> d['e'] = 2
        >>> 'a' in d
        True
        """
        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                return True
            h = (h+1) % self.capacity
        return False

    def __setitem__(self, k, v):
        """
        >>> # 1. test not contains
        >>> d = LinearProbingKVStore(capacity=2)
        >>> d['a'] = 1
        >>> d.keys
        [None, 'a']
        >>> # 2. test contains
        >>> d['a'] = 2
        >>> d.keys
        [None, 'a', None, None]
        >>> # 3. test resize up
        >>> d = LinearProbingKVStore(capacity=4)
        >>> d['a'] = 1
        >>> d['b'] = 1
        >>> d['c'] = 1
        >>> d.capacity
        8
        """
        if self.n * 2 >= self.capacity:
            self._resize(self.capacity*2)

        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                self.values[h] = v
                return
            h = (h+1) % self.capacity
        self.keys[h] = k
        self.values[h] = v
        self.n += 1

    def __iter__(self):
        """
        >>> d = LinearProbingKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> for i in d:
        ...     print i
        ...
        a
        b
        """
        for k in self.keys:
            if k is not None:
                yield k

    def items(self):
        """
        >>> d = LinearProbingKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 2
        >>> for k, v in d.items():
        ...     print k, v
        ...
        a 1
        b 2
        """
        for k, v in zip(self.keys, self.values):
            if k is not None:
                yield k, v

    def __getitem__(self, k):
        """
        >>> # 1. test key not exists
        >>> d = LinearProbingKVStore(capacity=2)
        >>> d['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> # 2. test key exists
        >>> d['a'] = 1
        >>> d['a']
        1
        >>> d['b']
        Traceback (most recent call last):
            ...
        KeyError: 'b'
        """
        h = self._hash(k)
        while self.keys[h] is not None:
            if self.keys[h] == k:
                return self.values[h]
            h = (h+1) % self.capacity
        raise KeyError(k)

    def __delitem__(self, k):
        """
        >>> # 1. test not contains
        >>> d = LinearProbingKVStore()
        >>> del d['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> # 2. test contains
        >>> d['a'] = 1
        >>> del d['a']
        >>> d['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> # 3. test rehash
        >>> d = LinearProbingKVStore()
        >>> d._hash('a')
        1
        >>> d._hash('e')
        1
        >>> d['a'] = 1
        >>> d['e'] = 2
        >>> d.keys
        [None, 'a', 'e', None]
        >>> del d['a']
        >>> d.keys
        [None, 'e', None, None]
        """
        h = self._hash(k)
        while True:
            if self.keys[h] is None:
                raise KeyError(k)
            if self.keys[h] == k:
                break
            h = (h+1) % self.capacity

        # delete
        self._delete_kv_at_index(h)

        # rehash the keys in same bucket
        h = (h+1) % self.capacity


        while self.keys[h] is not None:
            self._rehash(h)
            h = (h+1) % self.capacity

        # resize down
        if self.n and self.n * 8 <= self.capacity:
            self._resize(self.capacity/2)

    def _delete_kv_at_index(self, h):
        self.keys[h] = None
        self.values[h] = None
        self.n -= 1

    def _rehash(self, h):
        key = self.keys[h]
        value = self.values[h]
        self._delete_kv_at_index(h)

        self[key] = value

    def _hash(self, k):
        """
        >>> d = LinearProbingKVStore()
        >>> d._hash('a')
        1
        >>> d._hash('b')
        2
        >>> d._hash('c')
        3
        >>> d._hash('d')
        0
        """
        return sum(ord(i) for i in str(k)) % self.capacity

    def _resize(self, capacity):
        """
        >>> d = LinearProbingKVStore()
        >>> d['a'] = 1
        >>> d['b'] = 1
        >>> d.capacity
        4
        >>> d['c'] = 1
        >>> d.capacity
        8
        >>> del d['a']
        >>> del d['b']
        >>> d.capacity
        4
        """
        d = LinearProbingKVStore(capacity=capacity)
        for k, v in self.items():
            d[k] = v
        self.capacity = capacity
        self.keys = d.keys
        self.values = d.values
