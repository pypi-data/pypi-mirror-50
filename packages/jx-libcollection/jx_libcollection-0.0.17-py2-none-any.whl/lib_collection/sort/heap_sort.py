def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    n = len(lst)
    # make max priority queue
    for i in range(n/2, 0, -1):
        _sink(lst, i, n)

    # sort
    while n > 1:
        _exchange(lst, 1, n)
        n -= 1
        _sink(lst, 1, n)


def _sink(lst, i, n):
    while 2 * i <= n:
        j = 2 * i
        if j < n and _compare(lst, j, j+1) < 0:
            j += 1
        if _compare(lst, i, j) >= 0:
            break
        _exchange(lst, i, j)
        i = j


def _compare(lst, i, j):
    return lst[i-1] - lst[j-1]


def _exchange(lst, i, j):
    lst[i-1], lst[j-1] = lst[j-1], lst[i-1]
