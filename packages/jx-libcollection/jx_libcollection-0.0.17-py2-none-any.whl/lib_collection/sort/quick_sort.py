def sort(lst):
    """
    >>> lst = [5, 4, 3, 2, 1]
    >>> sort(lst)
    >>> lst
    [1, 2, 3, 4, 5]
    """
    _sort(lst, 0, len(lst)-1)


def _sort(lst, lo, hi):
    if lo >= hi:
        return

    p = partition(lst, lo, hi)
    _sort(lst, lo, p-1)
    _sort(lst, p+1, hi)


def partition(lst, lo, hi):
    value = lst[lo]

    left = lo + 1
    right = hi
    done = False

    while not done:
        while left <= right and lst[left] <= value:
            left += 1
        while left <= right and lst[right] >= value:
            right -= 1
        if right < left:
            done = True
        else:
            lst[left], lst[right] = lst[right], lst[left]
    lst[right], lst[lo] = lst[lo], lst[right]
    return right
