"""
    |--------|-----|---------------------------------|-------------------------------------------------|
    0      -/n1  -/n2                                n1                                               n2

    If primeString does not have enough digits, we will double the size of our sieve. All the primes 
    till n1 (inclusive) have been found. So first, I need to look at the primes located between 
    [2, sqrt(n1)]. For each one, I mark its multiples located between [n1, n2] as false. Then I can
    look at all the primes between [sqrt(1), sqrt(2)]. For each one, I mark its multiples false. The 
    good thing is, each of these are guaranteed to be greater than n1, so I don't need to figure the
    starting point. 
"""


import math

primeString: str = "2357"
primeNums: list[bool] = [False, False, True, True, False, True, False, True, False, False, False]
#                       [  0      1      2     3     4      5     6      7     8      9      10 ]

def solution(index):
    global primeString
    global primeNums

    while len(primeString) < (index + 5):
        
        # will be needed later
        n1 = len(primeNums) - 1
        primeNums.extend([True] * len(primeNums))   # double the size
        n2 = len(primeNums) - 1

        # cross off the multiples of primes from [2, sqrt(n1)]
        # located beyond n1
        i = 2
        while i <= math.floor(math.sqrt(n1)):
            if primeNums[i]:
                j = i*i + math.floor((float(n1)/float(i)) - i)*i
                while j <= n2:
                    primeNums[j] = False
                    j = j + i
            i = i + 1

        # cross of multiples of the primes between sqrt(n1) and sqrt(n2)
        # all these multiples are automatically located beyond n1
        i = math.floor(math.sqrt(n1))
        while i < math.floor(math.sqrt(n2)):
            if primeNums[i]:
                j = i*i
                while j <= n2:
                    primeNums[j] = False
                    j = j + i
            i = i + 1

        # update the string
        for i in range(n1 + 1, len(primeNums)):
            if primeNums[i]:
                primeString = primeString + str(i)
    
    return primeString[index : index + 5]


# This is adding in extra digits for some reason
