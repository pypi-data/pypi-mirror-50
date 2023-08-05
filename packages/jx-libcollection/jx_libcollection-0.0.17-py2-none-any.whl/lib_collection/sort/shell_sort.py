def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    sublist_count = len(lst) / 2
    while sublist_count > 0:
        for i in range(sublist_count):
            gap_insertion_sort(lst, i, sublist_count)
        sublist_count /= 2


def gap_insertion_sort(lst, start, gap):
    for i in range(start+gap, len(lst), gap):
        v = lst[i]
        j = i
        while j >= gap and lst[j-gap] > v:
            lst[j] = lst[j-gap]
            j -= gap
        lst[j] = v
