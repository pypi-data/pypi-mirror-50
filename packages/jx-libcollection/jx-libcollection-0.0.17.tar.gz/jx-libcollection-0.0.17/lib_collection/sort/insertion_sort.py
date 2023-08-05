def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    n = len(lst)
    for i in range(1, n):
        j = i
        v = lst[i]
        while j > 0 and lst[j-1] > v:
            lst[j] = lst[j-1]
            j -= 1
        lst[j] = v
