def sort(lst):
    """
    >>> lst = [6, 5, 4, 3, 2]
    >>> sort(lst)
    >>> lst
    [2, 3, 4, 5, 6]
    """
    n = len(lst)
    for slot in range(n-1, 0, -1):
        max_index = 0
        for i in range(1, slot+1):
            if lst[i] > lst[max_index]:
                max_index = i
        lst[max_index], lst[slot] = lst[slot], lst[max_index]
