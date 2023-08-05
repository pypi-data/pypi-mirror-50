def sort(lst):
    """
    >>> lst = [6, 5, 4, 3, 2]
    >>> sort(lst)
    >>> lst
    [2, 3, 4, 5, 6]
    """
    n = len(lst)
    done = False
    round = n - 1
    while not done and round:
        done = True
        for i in range(round):
            if lst[i] > lst[i+1]:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                done = False
                # if there is no swap, the list is sorted already
        round -= 1
