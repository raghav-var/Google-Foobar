def solution(x: str, y: str) -> str:
    # Your code here
    M = int(x)
    F = int(y)

    gens_passed = 0
    FACTOR_THRESHOLD = 0

    while True:
        # Terminating cases
        if M == 1 and F == 1:
            return str(gens_passed)
        if M < 1 or F < 1 or M == F:
            return "impossible"

        # Reducing Cases
        if M > F:
            # How many times F fits completely inside the additional M
            factor = (M - F) // F                     # = (M // F) - 1
            if factor > FACTOR_THRESHOLD:
                M -= factor * F
                gens_passed += factor
            else:
                M -= F
                gens_passed += 1
        else:
            # How many times M fits completely inside the additional F
            factor = (F - M) // M                     # = (F // M) - 1
            if factor > FACTOR_THRESHOLD:
                F -= factor * M
                gens_passed += factor
            else:
                F -= M
                gens_passed += 1
            


"""
I could have gotten to any point by either adding M bombs or F bombs.
Is there any way to dertermine which one would have occurred for sure?

Yes, whichever one there is more of must be the one that was added in the last generation.
    * Some mental examples illustrate this given the fact you always start with (1, 1)
If there is an equal amount, that implies there were 0 of one if the last gen, which is impossible
    * Unless it's (1, 1), which is the starting point

Apparently failing test case 3 is a speed issue.
To speed it up, if the number of one of them is more than thrice the other, then I can just 
jump down multiple generations at once. If it's just twice more, then one generation will 
already do the trick.

Normally, I just want to reduce Greater by ((Greater // Lesser) * Lesser)
This will work fine as long as (Greater / Lesser) is not an integer and has some
decimal portion. But if it is exactly an integer, I will end up reducing Greater to 0
instead of bringing both to the quanity of Lesser. The current code should avoid this problem.
I wonder if there is a way to do the same thing but with code that looks better.
"""