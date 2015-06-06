__author__ = 'luiz'

import numpy as np


def lev(s1, s2, i, j):
    print (i, j)

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

    tam1 = len(s1)
    tam2 = len(s2)

    M = np.zeros(shape=(tam1 + 1, tam2 + 1), dtype=np.int16)

    M[:, 0] = np.array([i for i in range(tam1 + 1)])
    M[0, :] = np.array([i for i in range(tam2 + 1)])

    # computes the edits distance matrix using DP
    for i in range(1, tam1 + 1):
        for j in range(1, tam2 + 1):
            M[i, j] = min([
                (s1[i - 1] != s2[j - 1]) + M[i - 1, j - 1],
                M[i, j - 1] + 1,
                M[i - 1, j] + 1
            ])

    # Backtracks it to find the edit operations
    edits1 = edits2 = list()

    g

    i, j = tam1 - 1, tam2 - 1
    while i >= 0 and j >= 0:

        """
           Discovers what kind of operation was performed:
             0 = replacing or leaving
             1 = deletion from s1
             2 = deletion from s2
        """
        op_type = np.argmin([
            (s1[i - 1] != s2[j - 1]) + M[i - 1, j - 1],
            M[i, j - 1] + 1,
            M[i - 1, j] + 1
        ])

        if op_type == 0:
            i -= 1
            j -= 1
            print 'a'

            print 'Diagonal %c, %c @ %d %d' % (s1[i], s2[j], i, j)
            if s1[i] == s2[j]:
                edits1.extend(s1[i])
                edits2.extend(s2[j])
            else:
                # if the chars aren't equal, then it is a substitution. Signalizes this surrounding the char with []
                # edits1.extend(('[', s1[i], ']'))
                # edits2.extend(('[', s2[j], ']'))

                edits1.extend((s1[i]))
                edits2.extend((s2[j]))
        elif op_type == 1:
            j -= 1

            print 'b'
            print 'Left %c, %c @ %d %d' % (s1[i], s2[j], i, j)

            edits1.append('-')
            edits2.append(s2[j])

        else:
            i -= 1

            print 'c'
            print 'Up %c, %c @ %d %d' % (s1[i], s2[j], i, j)

            edits1.append(s1[i])
            edits2.append('-')

    return M[tam1, tam2], edits1, edits2


s1 = "Seven"
s2 = "Evening"
s1, s2 = s2, s1


edits, e1, e2 = lev_dp(s1, s2)
print edits
print ''.join(e1)
print ''.join(e2)