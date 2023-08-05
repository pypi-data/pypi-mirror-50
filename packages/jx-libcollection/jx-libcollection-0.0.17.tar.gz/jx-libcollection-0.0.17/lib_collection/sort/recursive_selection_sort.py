def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    _sort(lst, len(lst)-1)


def _sort(lst, slot):
    if slot == 0:
        return
    max_index = slot
    for i in range(slot):
        if lst[i] > lst[max_index]:
            max_index = i
    lst[max_index], lst[slot] = lst[slot], lst[max_index]
    _sort(lst, slot-1)
