from fractions import Fraction
import numpy as np

"""
Solution based on: https://math.dartmouth.edu/archive/m20x06/public_html/Lecture14.pdf

I realized that this was a graph-problem while in the shower, and some online searches
showed that it has a name: absorption probbailities for Absorbing Markov Chains. NGL
for some reason I though it was a dynamic programming problem at first, but the 
existence of loops completely destroys that.
"""

def getCanonical(matrix: list[list[int]]) -> tuple[list[list[Fraction]], int]:
    """
    I'm making the assumption that all the terminal states are
    at the bottom. Let's see if it is a correct assumption. The function
    returns the canonical form of the input in fractional form as well
    as the number of absorbing states found.
    """
    can_mat = [([None] * len(matrix[0])) for i in range(len(matrix))]
    absorbing = 0
    for r in range(0, len(matrix)):
        if sum(matrix[r]) == 0: # is an absorbing state
            absorbing += 1
            for c in range(0, len(matrix[r])):
                can_mat[r][c] = Fraction(0, 1)
            can_mat[r][r] = Fraction(1, 1)
        else:
            for c in range(0, len(matrix[r])):
                can_mat[r][c] = Fraction(matrix[r][c], sum(matrix[r]))
    return can_mat, absorbing


def invertMatrix(matrix: np.ndarray) -> np.ndarray:
    """
    Can't use the numpy.linalg.inv() function since the elements 
    are Fractions. So I'm going to implement my own algorithm to 
    do this.
    """
    return


def solution(m: list[list[int]]) -> list[int]:
    """
    I need to find the absorption probabilties for this Markov chain.
    This can be done by finding B = NR, where N is the fundamental
    matrix and R is a portion from the canonical form.
    """
    # Let's have a simple check to get rid of 1x1 matrices
    if len(m) == 1:
        return [1, 1]

    # First, let's obtain the Canonical form
    canonical, num_absorptions = getCanonical(m)
    canonical = np.array(canonical)

    # Now we can obtain Q and R
    Q = canonical[0:(len(canonical) - num_absorptions), 0:(len(canonical) - num_absorptions)]
    R = canonical[0:(len(canonical) - num_absorptions), (len(canonical) - num_absorptions):(len(canonical[0]))]
    
    # Calculate N = (I - Q)^(-1)
    I = np.identity(len(Q), dtype=int).tolist()     # generate identity matrix as 2D list
    I, trash = getCanonical(I)                      # reuse function to convert to fractions
    I = np.array(I)                                 # Convert back to np.array
    N = invertMatrix(I - Q)                         # Calculate N

    # return I, Q, I - Q
    return
