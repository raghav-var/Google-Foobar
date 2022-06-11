from fractions import Fraction, gcd
import numpy as np

"""
Solution based on: https://math.dartmouth.edu/archive/m20x06/public_html/Lecture14.pdf

This is basically an absorbing Markov Chain problem
"""

def getCanonical(matrix):
    """
    I'm making the assumption that all the terminal states are
    at the bottom. Let's see if it is a correct assumption. The function
    returns the canonical form of the input in fractional form as well
    as the number of absorbing states found. Does not modify input, instead
    it returns a new object.

    I think the problem might be that the terminating states aren't
    ALWAYS at the bottom. Gonna fix that now

    I'm also using this function to convert identity matrices to 
    fractionla form. Def a waste of computation but whatever.

    S0 will always be first row since if S0 is terminal, this 
    function will not have been called at all
    """

    terminals = []
    num_terminals = 0
    transients = []
    num_transients = 0
    swaps = [None] * len(matrix)

    # Rearrange rows so all terminal states are at end of matrix
    # relative ordering within the categories is maintained
    for r in range(0, len(matrix)):
        if (sum(matrix[r]) != 0) and (sum(matrix[r]) != matrix[r][r]):
            transients.append(matrix[r])
            swaps[r] = num_transients
            num_transients += 1
    for r in range(0, len(matrix)):
        if (sum(matrix[r]) == 0) or (sum(matrix[r]) == matrix[r][r]):
            terminals.append(matrix[r])
            swaps[r] = num_transients + num_terminals
            num_terminals += 1
    temp = transients + terminals

    # Now I need to switch the columns based on the new row positions
    temp = np.array(temp)
    temp2 = np.copy(temp)
    for i in range(0, len(swaps)):
        temp2[:, swaps[i]] = temp[:, i]
    temp2 = temp2.tolist()

    # Now convert the rows into fractions and standardize the 
    # represnetation of terminals
    can_mat = [([None] * len(temp2[0])) for i in range(len(temp2))]

    for r in range(0, len(temp2)):
        if r < num_transients:
            for c in range(0, len(temp2[0])):
                can_mat[r][c] = Fraction(temp2[r][c], sum(temp2[r]))
        else:
            for c in range(0, len(temp2[0])):
                can_mat[r][c] = Fraction(0, 1)
            can_mat[r][r] = Fraction(1, 1)
    
    # Return all the important information
    return can_mat, num_terminals


def toRREF(M):
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


def inverseMatrix(matrix):
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
    AwithI = np.concatenate((A, I), axis=1)         # Gives [ A | I ] as a new object PROBLEM from CONCATENATE?

    # Need to use Gauss-Jordan elimination, to do: [ A | I ] -> [ I | A^-1 ]
    # Just go to RREF and extract right half
    toRREF(AwithI)
    A_inv = AwithI[:, len(A[0]):len(AwithI[0])]

    return A_inv


def solution(m):
    """
    I need to find the absorption probabilties for this Markov chain.
    This can be done by finding B = NR, where N is the fundamental
    matrix and R is a portion from the canonical form.
    """
    # Wacky cases
    if sum(m[0]) == m[0][0]:
        # S0 is terminal, just count up how many others there are
        count = 0
        for r in range(0, len(m)):
            if sum(m[r]) == m[r][r]:
                count += 1
        gross = [0] * count
        gross[0] = 1
        gross.append(1)
        return gross
    elif len(m) == 1:
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

    """
    Basically the big problem seemed to be that not all tets cases had
    terminating states at the bottom. So I needed to swap the rows
    (and then the columns) to get everything in canonical form while
    preserving the relative order within the categories. This would allow
    the matrix method to work. The only problem was if the starting state
    was terminal. While converting to canonical form, it would get put 
    below the transient stages, and the matrix method only shows 
    absorption probablities for when you start at a transient stage. So
    to handle this, I added a base case in the solution() function.
    In every other case, the starting state S0 will be transient and 
    end up in the first row of the canonical matrix. And so when I get
    the B matrix, I can just look at its first row.

    ALso in Python 3, gcd is from the math library instead of fractions
    """
