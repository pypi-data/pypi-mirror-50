def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    n = len(lst)
    for i in range(n-1, 0, -1):
        for j in range(i-1, -1, -1):
            if lst[j] > lst[i]:
                lst[j], lst[i] = lst[i], lst[j]
