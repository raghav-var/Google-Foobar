from typing import Callable

# MergeSort Class Definition Start ================================================

class MergeSort:
    # Store the comparator function
    _less: Callable = None

    # Helper functions
    def _merge(self, list_in: list, begin: int, middle: int, end: int) -> None:
        temp = []
        i = begin
        j = middle
        while ( (i < middle) and (j < end) ):
            if self._less(list_in[i], list_in[j]):
                temp.append(list_in[i])
                i += 1
            else:
                temp.append(list_in[j])
                j += 1
        while (i < middle):
            temp.append(list_in[i])
            i += 1
        while (j < end):
            temp.append(list_in[j])
            j += 1
        for idx in range(0, len(temp)):
            list_in[begin + idx] = temp[idx]
        return

    def _mergesort_helper(self, list_in: list, begin: int, end: int) -> None:
        if ((end - begin) <= 1):
            return
        else:
            middle = ((end - begin) // 2) + begin
            self._mergesort_helper(list_in, begin, middle)
            self._mergesort_helper(list_in, middle, end)
            self._merge(list_in, begin, middle, end)
            return

    # Default comparator defined internally
    def _lessThan(lhs, rhs) -> bool:
        return lhs <= rhs

    # Constructor and Call
    def __init__(self, comp: Callable = _lessThan) -> None:
        self._less = comp
        return
    
    def __call__(self, list_in: list) -> None:
        self._mergesort_helper(list_in, 0, len(list_in))
        return

# MergeSort Class Definition End ==================================================


def olderVer(lhs: str, rhs: str) -> bool:
    # Use these as a tie-breaker if needed
    lhs_len = len(lhs) 
    rhs_len = len(rhs)
    # Holy crap Louis, Python literally has a built-in function for everything
    # Convert string into list of ints
    lhs = list(map(int, lhs.split('.')))
    rhs = list(map(int, rhs.split('.')))
    lidx = 0
    ridx = 0
    # Iterate checking most significant numbers first
    while (lidx < len(lhs)) and (ridx < len(rhs)):
        if lhs[lidx] != rhs[ridx]:
            return lhs[lidx] < rhs[ridx]
        lidx += 1
        ridx += 1
    # Getting here means one is shorter than the other (or same numerical values)
    # So now I can use their string lengths from before
    return lhs_len <= rhs_len

def solution(l: list[str]) -> None:
    sort = MergeSort(olderVer)
    sort(l)
    return
