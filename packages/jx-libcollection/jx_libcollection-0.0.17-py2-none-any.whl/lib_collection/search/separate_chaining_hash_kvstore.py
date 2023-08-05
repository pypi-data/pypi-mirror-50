from lib_collection.search.sequential_search_kvstore import (
    SequentialSearchKVStore,
)


class SeparateChainingHashKVStore(object):

    __item_cnt_per_bucket__ = 10

    def __init__(self, d=None, bucket_cnt=4):
        """
        >>> h = SeparateChainingHashKVStore({'c': 3, 'b': 2, 'a': 1})
        >>> h['a']
        1
        >>> h['b']
        2
        >>> h['c']
        3
        """
        self.n = 0
        self.bucket_cnt = bucket_cnt
        self.lst = [SequentialSearchKVStore() for _ in range(self.bucket_cnt)]
        if d:
            s = SeparateChainingHashKVStore(bucket_cnt=bucket_cnt)
            for k, v in d.items():
                s[k] = v
            self.n = s.n
            self.bucket_cnt = s.bucket_cnt
            self.lst = s.lst

    def __repr__(self):
        """
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> h['c'] = 3
        >>> h
        SeparateChainingHashKVStore({'c': 3, 'b': 2, 'a': 1})
        """
        s = ', '.join(
            '{}: {}'.format(repr(k), repr(v))
            for k, v in self.items()
        )
        return 'SeparateChainingHashKVStore({%s})' % s

    def __len__(self):
        """
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> len(h)
        0
        >>> h['a'] = 1
        >>> h['b'] = 2
        >>> h['c'] = 3
        >>> len(h)
        3
        >>> del h['c']
        >>> len(h)
        2
        """
        return self.n

    def __iter__(self):
        """
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> h['a'] = 2
        >>> h['b'] = 1
        >>> h['c'] = 3
        >>> for k in h:
        ...     print k
        ...
        c
        b
        a
        """
        for kvstore in self.lst:
            for k in kvstore:
                yield k

    def __contains__(self, k):
        """
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> 'a' in h
        False
        >>> h['a'] = 1
        >>> 'a' in h
        True
        """
        i = self._hash(k)
        d = self.lst[i]
        return k in d

    def items(self):
        """
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> h['a'] = 2
        >>> h['b'] = 1
        >>> h['c'] = 3
        >>> for k, v in h.items():
        ...     print k, v
        ...
        c 3
        b 1
        a 2
        """
        for kvstore in self.lst:
            for k, v in kvstore.items():
                yield k, v

    def __setitem__(self, k, v):
        """
        >>> # 1. test not contains
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> len(h)
        0
        >>> h['a'] = 1
        >>> len(h)
        1
        >>> 'a' in h.lst[0]
        True
        >>> # 2. test contains
        >>> h = SeparateChainingHashKVStore(bucket_cnt=1)
        >>> s = SequentialSearchKVStore()
        >>> s['a'] = 1
        >>> h.n = 1
        >>> h.lst = [s]
        >>> h['a'] = 2
        >>> len(h)
        1
        >>> s['a']
        2
        >>> # 3. test resize up
        >>> h = SeparateChainingHashKVStore(bucket_cnt=4)
        >>> h.n = 40
        >>> h['a'] = 1
        >>> h.bucket_cnt
        8
        """
        if self.n >= 10 * self.bucket_cnt:
            self._resize(self.bucket_cnt*2)

        i = self._hash(k)
        d = self.lst[i]
        if k not in d:
            self.n += 1
        d[k] = v

    def __getitem__(self, k):
        """
        >>> # 1. test contains
        >>> h = SeparateChainingHashKVStore()
        >>> h['a'] = 1
        >>> h['a']
        1
        >>> # 2. test not contains
        >>> h = SeparateChainingHashKVStore()
        >>> h['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        """
        i = self._hash(k)
        d = self.lst[i]
        return d[k]

    def __delitem__(self, k):
        """
        >>> # 1. test contains
        >>> h = SeparateChainingHashKVStore()
        >>> h['a'] = 1
        >>> del h['a']
        >>> h['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        >>> # 2. test not contains
        >>> h = SeparateChainingHashKVStore()
        >>> del h['a']
        Traceback (most recent call last):
            ...
        KeyError: 'a'
        """
        i = self._hash(k)
        d = self.lst[i]
        if k in d:
            self.n -= 1
        del d[k]

    def _hash(self, k):
        """
        >>> d = SeparateChainingHashKVStore()
        >>> d._hash('a')
        1
        >>> d._hash('b')
        2
        >>> d._hash('c')
        3
        >>> d._hash('d')
        0
        """
        return sum(ord(i) for i in str(k)) % self.bucket_cnt

    def _resize(self, bucket_cnt):
        s = SeparateChainingHashKVStore(bucket_cnt=bucket_cnt)
        for k, v in self.items():
            s[k] = v
        self.bucket_cnt = bucket_cnt
