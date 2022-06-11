from fractions import Fraction
from math import gcd
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
    as the number of absorbing states found. Does not modify input, instead
    it returns a new object.
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


def toRREF(M: np.ndarray) -> None:
    """
    Function modifies input array to be in reduced row echelon form
    Pseudocode from: https://en.wikipedia.org/wiki/Row_echelon_form
    Currently provides no indication if the matrix isn't invertible
    and quits partway through the calculation. Problem?
    """
    lead = 0
    rowCount = len(M)
    colCount = len(M[0])

    for r in range(0, rowCount):
        if colCount <= lead:
            return
        i = r
        while M[i, lead] == 0:
            i = i + 1
            if rowCount == i:
                i = r
                lead = lead + 1
                if colCount == lead:
                    return
        if i != r:  M[[i, r], :] = M[[r, i], :] # swap rows i and r
        M[r, :] = M[r, :] / M[r, lead]
        for j in range(0, rowCount):
            if j != r:
                M[j, :] = M[j, :] - (M[j, lead] * M[r, :])
        lead = lead + 1
    return


def inverseMatrix(matrix: np.ndarray) -> np.ndarray:
    """
    Can't use the numpy.linalg.inv() function since the elements 
    are Fractions. So I'm going to implement my own algorithm to 
    do this. Method: Gauss-Jordan Elimination.
    Does not modify input, returns new object instead.
    """
    # Base case
    if len(matrix) == 1:
        if matrix[0][0] == 0:
            return None # Inverse DNE
        else:
            return np.array([[Fraction(1, matrix[0][0])]])

    # Okay, generate Identity matrix and concatenate it on right
    A = matrix                                      # improve readability
    I = np.identity(len(A), dtype=int).tolist()     # Generate identity matrix
    I, trash = getCanonical(I)                      # convert to fractions
    I = np.array(I)                                 # convert back to np.ndarray
    AwithI = np.concatenate((A, I), axis=1)         # Gives [ A | I ] as a new object

    # Need to use Gauss-Jordan elimination, to do: [ A | I ] -> [ I | A^-1 ]
    # Just go to RREF and extract right half
    toRREF(AwithI)
    A_inv = AwithI[:, len(A[0]):len(AwithI[0])]

    return A_inv


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

    # Now we can obtain Q and R (these are simply refernces, not copies)
    Q = canonical[0:(len(canonical) - num_absorptions), 0:(len(canonical) - num_absorptions)]
    R = canonical[0:(len(canonical) - num_absorptions), (len(canonical) - num_absorptions):(len(canonical[0]))]
    
    # Calculate N = (I - Q)^(-1)
    I = np.identity(len(Q), dtype=int).tolist()     # generate identity matrix as 2D list
    I, trash = getCanonical(I)                      # reuse function to convert to fractions (sus)
    I = np.array(I)                                 # Convert back to np.ndarray
    N = inverseMatrix(I - Q)                        # Calculate N

    # Calculate B = NR
    B = np.matmul(N, R)

    # Find lowest common denominator of first row (LCM of denominators)
    lcd = B[0][0].denominator
    for i in range(1, len(B[0])):
        lcd = (lcd * B[0][i].denominator) // gcd(lcd, B[0][i].denominator)
    
    # make the output array
    out = []
    for elem in B[0]:
        out.append(elem.numerator * (lcd // elem.denominator))
    out.append(lcd)

    return out
