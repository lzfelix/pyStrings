__author__ = 'luiz'

import numpy as np


def lev(s1, s2, i, j):
    """
    Computes the recursive Levenshtein Distance. Deprecated by lev_dp().

    :param s1: The first string to be used in the comparison (won't be modified)
    :param s2: The first string to be used in the comparison (won't be modified)
    :param i: should be len(s1) - 1
    :param j: should be len(s2) - 1

    :return: The cost for transforming s1 into s2 and vice-versa. The costs for the deletion, replacement and insertion
    operations is 1.
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


def lev_dp(s1, s2):
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

    def compare_chars(s1, s2, i, j):
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

    tam1 = len(s1)
    tam2 = len(s2)

    M = np.zeros(shape=(tam1 + 1, tam2 + 1), dtype=np.int16)

    M[:, 0] = np.array([i for i in range(tam1 + 1)])
    M[0, :] = np.array([i for i in range(tam2 + 1)])

    # computes the edits distance matrix using DP
    for i in range(1, tam1 + 1):
        for j in range(1, tam2 + 1):
            M[i, j] = min([
                compare_chars(s1, s2, i - 1, j - 1) + M[i - 1, j - 1],
                M[i, j - 1] + 1,
                M[i - 1, j] + 1
            ])

    edits1 = list()
    edits2 = list()

    i, j = tam1, tam2
    while i > 0 and j > 0:
        """
           Discovers what kind of operation was performed (the one with lesser cost):
             0 = replacing or leaving (diagonal)
             1 = deletion from s1 (left)
             2 = deletion from s2 (up)
        """

        op_type = np.argmin([
            compare_chars(s1, s2, i - 1, j - 1) + M[i - 1, j - 1],
            M[i, j - 1] + 1,
            M[i - 1, j] + 1
        ])

        # print('Appended %d. comparing %c and %c' % (op_type, s1[i - 1], s2[j - 1]))

        if op_type == 0:
            if s1[i - 1] == s2[j - 1]:
                edits1.extend(s1[i - 1])
                edits2.extend(s2[j - 1])
            else:
                # if the chars aren't equal, then it is a substitution. Signalizes this surrounding the char with []
                # the string will be reversed, that's why the brackets are reversed =)
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

    if i > 0 and j <= 0:
        edits1.extend(s1[0:i])
        edits2.extend(len(s1[0:i]) * '-')
    elif j > 0 and i <= 0:
        edits1.extend(len(s2[0:j]) * '-')
        edits2.extend(s2[0:j])

    edits1.reverse()
    edits2.reverse()
    return M[tam1, tam2], ''.join(edits1), ''.join(edits2)


if __name__ == "__main__":

    s1 = "Evening"
    s2 = "Seven"

    cost, edt1, edt2 = lev_dp(s1, s2)
    print edt1
    print edt2
    print 'Total cost: %d' % cost

    # print lev(s1, s2, len(s1) - 1, len(s2) - 1)