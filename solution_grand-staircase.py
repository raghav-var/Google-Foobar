memo = None

def memo_access(r, c):
    global memo
    # Check if filled
    if memo[r][c] != None:
        return memo[r][c]
    # If not, have to do work
    memo[r][c] = memo_access(r - 1, c)
    if c >= r:
        memo[r][c] += memo_access(r - 1, c - r)
    return memo[r][c]

def solution(n):
    global memo
    # Initialize the memo
    memo = [[None] * (n + 1) for i in range(n + 1)]
    memo[0] = [1] + [0] * n
    # Call the recursive function
    return memo_access(n, n) - 1


"""
    I knew this was Dnyamic Programming, but I was still unsure where to begin.

    So after some digging it seems this has to do with distinct partitions. Such a partition 
    is just writing N as a sum of postive integers only, where no integer occurs more than once. 
    Partitions already do not care for order, so two partitions are distinct only if the sets 
    of their summing integers are different. 

    The important thing is, that for any one partition, there is only one way to form a staircase 
    with those heights that satisifes the given constraints. It has to be in decreasing order, 
    and there will only be one such sequence for a set of numbers with no repetitions.

    Source: https://en.wikipedia.org/wiki/Partition_%28number_theory%29#Odd_parts_and_distinct_parts

    So then I can just implement that formula for the number of distinct partitions and use a memo
    with DP to reduce the workload.

    Yes I used a global variable. But it's python, so it's limited to this file
    unless someone EXPLICITLY decides to mess with it, in which case it's their
    problem.
"""