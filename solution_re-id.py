import math

primeNums: list[bool] = [True] * 20232
primeString: str = ""
calledB4: bool = False

def solution(index):
    global primeNums
    global primeString
    global calledB4

    if not calledB4:
        calledB4 = True
        i = 2
        while i <= math.floor(math.sqrt(len(primeNums) - 1)):
            if primeNums[i]:
                j = i*i
                while j <= (len(primeNums) - 1):
                    primeNums[j] = False
                    j = j + i
            i = i + 1

        for i in range(2, len(primeNums)):
            if primeNums[i]:
                primeString = primeString + str(i)
    
    return primeString[index : index + 5]
