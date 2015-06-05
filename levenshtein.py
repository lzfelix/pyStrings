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

    for i in range(1, tam1 + 1):
        for j in range(1, tam2 + 1):

            # if s1[i - 1] == s2[j - 1]:
            #     diff = 0
            # else:
            #     diff = 1

            M[i, j] = min([
                (s1[i - 1] != s2[j - 1]) + M[i - 1, j - 1],
                M[i, j - 1] + 1,
                M[i - 1, j] + 1
            ])

    return M[tam1, tam2]


s1 = "Seven"
s2 = "Evening"
s1, s2 = s2, s1

print lev_dp(s1, s2)