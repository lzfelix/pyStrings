__author__ = 'luiz'

import numpy as np


def __compare_chars(s1, s2, i, j):
        """
        Helper function to compare if two chars in different strings are DIFFERENT. This function exists to avoid the
        behavior s[-1] == s[len(s) - 1].

        :param s1: The first collection of chars (string).
        :param s2: The second collection of chars (string).
        :param i: The position of s1 to be compared to s2
        :param j: The position of s2 to be compared to s1

        :return: 1 if any index is lesser than 0, otherwise returns 0
        """

        if i < 0 or j < 0 or s1[i] != s2[j]:
            return 1
        return 0


def levenshtein_recursive(s1, s2):
    """
    Computes the recursive Levenshtein Distance. Deprecated, instead use levenshtein_dp() or levenshtein_sort() .

    :param s1: The first string to be used in the comparison (won't be modified)
    :param s2: The first string to be used in the comparison (won't be modified)

    :return: The cost for transforming s1 into s2 and vice-versa. The costs for the deletion, replacement and insertion
    operations are 1.
    """

    def lev(s1, s2, i, j):
        """
        This is the true Levenshtein recursive function.

        :param s1: The first string to be used in the comparison (won't be modified)
        :param s2: The first string to be used in the comparison (won't be modified)
        :param i: Must be len(s1) - 1
       :param j: Must be len(s2) - 1
        """

        if i == 0:
            return j

        if j == 0:
            return i

        if s1[i] == s2[j]:
            same = 0
        else:
            same = 1

        return min([1 + lev(s1, s2, i - 1, j), 1 + lev(s1, s2, i, j - 1), lev(s1, s2, i - 1, j - 1) + same])
    # function body

    # skip trivial cases
    if len(s1) == 0:
        return len(s2)

    if len(s2) == 0:
        return len(s1)

    # calculatations for the regular case
    return lev(s1, s2, len(s1) - 1, len(s2) - 1)


def levenshtein_dp(s1, s2):
    """
    Given two strings, computes the cost of transforming one into other by doing insertions, deletions and changing
    characters. The costs for all operations is 1 (but this could be changed). This method uses Dynamic Programming.

    :param s1: The first string to be used in the comparison (won't be modified)
    :param s2: The first string to be used in the comparison (won't be modified)

    :return: A triple (x,y,z) where x is the cost for transforming s1 into s2 (and vice-versa). y contains the
    modifications that must be made on s1 in order to turn it into s2. Plain characters on y means that this char
    must remain the same, '-' represents the deletion of the character on the original string and [c] means that the
    character c in this position was replaced by another character of s2.
    The same information happens for z in respect of s1.
    """

    tam1 = len(s1)
    tam2 = len(s2)

    M = np.zeros(shape=(tam1 + 1, tam2 + 1), dtype=np.int16)

    M[:, 0] = np.array([i for i in range(tam1 + 1)])
    M[0, :] = np.array([i for i in range(tam2 + 1)])

    # computes the edits distance matrix using DP
    for i in range(1, tam1 + 1):
        for j in range(1, tam2 + 1):
            M[i, j] = min([
                __compare_chars(s1, s2, i - 1, j - 1) + M[i - 1, j - 1],
                M[i, j - 1] + 1,
                M[i - 1, j] + 1
            ])

    edits1 = list()
    edits2 = list()

    # backtracks the matrix to find out how to transform the strings

    i, j = tam1, tam2
    while i > 0 and j > 0:
        """
           Discovers what kind of operation was performed (the one with lesser cost):
             0 = replacing or leaving (diagonal)
             1 = deletion from s1 (left)
             2 = deletion from s2 (up)

             This is performed from the solution to the beginning
        """

        op_type = np.argmin([
            __compare_chars(s1, s2, i - 1, j - 1) + M[i - 1, j - 1],
            M[i, j - 1] + 1,
            M[i - 1, j] + 1
        ])

        if op_type == 0:
            if s1[i - 1] == s2[j - 1]:
                edits1.extend(s1[i - 1])
                edits2.extend(s2[j - 1])
            else:
                # if the chars aren't equal, then it is a substitution. Signalizes this surrounding the char with []
                # the string will be reversed, that's why the brackets are reversed
                edits1.extend((']', s1[i - 1], '['))
                edits2.extend((']', s2[j - 1], '['))

            i -= 1
            j -= 1
        elif op_type == 1:
            edits1.extend('-')
            edits2.extend(s2[j - 1])

            j -= 1
        else:
            edits1.extend(s1[i - 1])
            edits2.extend('-')

            i -= 1

    # if remaining characters exists, them into the transformed strings
    if i > 0 and j <= 0:
        edits1.extend(s1[0:i])
        edits2.extend(len(s1[0:i]) * '-')
    elif j > 0 and i <= 0:
        edits1.extend(len(s2[0:j]) * '-')
        edits2.extend(s2[0:j])

    edits1.reverse()
    edits2.reverse()

    return M[tam1, tam2], ''.join(edits1), ''.join(edits2)


def needleman_wunsch(s1, s2):
    """
    Given two strings calculate all the best possible alignments between them. The traditional scoring system is used, so
    mismatches and indels receive -1 points and matches worth 2 poins.

    :param s1: The first string to be compared (can be a DNA sequence!)
    :param s2: The second string to be compared (can be a DNA sequence!)

    :return: A list of lists in the form [[a1, a2], [b1, b2], ...] where a1, a2 corresponds to an allignment and so on.
    The amount of alignments can be found by calculating the size of the bigger list.
    """

    # Simply adds a [char] to the beginning of [string]
    def append_t_strings(char, string):
        return [char + element for element in string]

    # Returns 1 if [char1] == [char2], -1 otherwise. If you want to change the score system, chance these values
    # (or multiply this function' calls by weights
    def comparison(char1, char2):
        if char1 == char2:
            return 1
        return -1

    # Backtracks the DP matrix in order to calculate all possible alignments between s1 and s2
    # (the returned sequences must be reversed)
    def find_sequences(i, j):

        # If the backtracking reached the leftmost column, there's nothing to append.
        if i == 0 and j == 0:
            return [['', '']]

        if i == 0:
            return [['', s2[j::-1]]]

        if j == 0:
            return [[s1[i::-1], '']]

        c = comparison(s1[i - 1], s2[j - 1])

        max_score = max(
            M[i - 1, j - 1] + c,
            M[i, j - 1] - 1,
            M[i - 1, j] - 1
        )

        path_diagonal = []
        path_up = []
        path_left = []

        # branching

        if M[i - 1, j - 1] + c == max_score:
            path_diagonal = find_sequences(i - 1, j - 1)
            path_diagonal = [[s1[i - 1] + element[0], s2[j - 1] + element[1]] for element in path_diagonal]

        if M[i, j - 1] - 1 == max_score:
            path_left = find_sequences(i, j - 1)
            path_left = [['-' + element[0], s2[j - 1] + element[1]] for element in path_left]

        if M[i - 1, j] - 1 == max_score:
            path_up = find_sequences(i - 1, j)
            path_up = [[s1[i - 1] + element[0], '-' + element[1]] for element in path_up]

        # merging
        return path_diagonal + path_up + path_left
    # function end

    tam1 = len(s1)
    tam2 = len(s2)

    M = np.zeros(shape=(tam1 + 1, tam2 + 1))

    M[0, :] = np.array(range(0, -tam2 - 1, -1))
    M[:, 0] = np.array(range(0, -tam1 - 1, -1))

    # simple Needleman-Wunsch's algorithm core
    for i in range(1, tam1 + 1):
        for j in range(1, tam2 + 1):
            M[i, j] = max(
                M[i - 1, j - 1] + comparison(s1[i - 1], s2[j - 1]),
                M[i, j - 1] - 1,
                M[i - 1, j] - 1
            )

    solutions = find_sequences(tam1, tam2)
    for solution in solutions:
        solution[0] = solution[0][::-1]
        solution[1] = solution[1][::-1]

    return solutions


def levenshtein_short(s1, s2, minimize_space=True):
    """
    Performs the Levenshtein's algorithm for calculating the cost of transforming s1 into s2 (and vice versa) using the
    DP shortened version, so instead of keeping the entire matrix on memory, just the previous and current lines are
    kept. Because of this, it is impossible to find out which operations must be performed in order to achieve the
    conversion.

    :paam s1: The first string to be used in the comparison (won't be modified)
    :param s2: The first string to be used in the comparison (won't be modified)
    :param minimize_space: default is True, so the space complexity will be O(min{len(s1), len(s2)}, if false this
     complexity becomes O(len(s2))
    :return: The cost for transforming s1 into s2 and vice versa. The allowed operations are: insertion, deletion and
    modification of characters. All the operations have unitary cost.
    """

    tam1 = len(s1)
    tam2 = len(s2)

    # so the line will have the size of the smallest word, but the number of iterations will increase
    if minimize_space and tam1 > tam2:
        tam1, tam2 = tam2, tam1
        s1, s2 = s2, s1

    M = np.zeros(shape=(2, tam2 + 1))
    M[0, :] = np.array([i for i in range(0, tam2 + 1)])

    for i in range(1, tam1 + 1):
        if i % 2 == 0:
            previous_i = 1
        else:
            previous_i = 0

        M[i % 2, 0] = i

        for j in range(1, tam2 + 1):
            M[i % 2, j] = min(
                __compare_chars(s1, s2, i - 1, j - 1) + M[previous_i, j - 1],
                M[i % 2, j - 1] + 1,
                M[previous_i, j] + 1
            )

    return M[tam1 % 2, tam2]


if __name__ == "__main__":

    s1 = 'GATTACA'
    s2 = 'GCATGCU'

    print("Aligning %s and %s using Needleman-Wunsch algorithm:" % (s1, s2))
    print(needleman_wunsch(s1, s2))

    s1 = "evening"
    s2 = "seven"

    print("Calculating Levenshtein (or edit) Distance between %s and %s" % (s1, s2))

    cost, edt1, edt2 = levenshtein_dp(s1, s2)
    print(edt1)
    print(edt2)
    print('Total cost (using DP): %d' % cost)

    print('Total cost (using abbreviated DP): %d' % levenshtein_short(s1, s2, False))

    print('Total cost (using the recursive method): %d' % levenshtein_recursive(s1, s2))
