# pyStrings

[![Build Status](https://travis-ci.org/lzfelix/pyStrings.svg?branch=master)](https://travis-ci.org/lzfelix/pyStrings)

A repository containing some Dynamic Programming String algorithms. For now the following methods were implemented:

_consider s1 and s2 as two different strings_.

* __Levenshtein distance__ (recursive);
* __Levenshtein distance__ (DP): An alternative implementation using Dynamic Programming. Also returns the operations that must be performed in order to transform _s1_ into _s2_ and vice-versa;
* __Levenshtein shortened version__ (DP): Instead of keeping the entire matrix M used on the standard Levenshtein Distance, this method keeps just the last two lines, so its space complexity is reduced to O(_min{len(s1), len(s2)}_), albeit the transforming operations can't be found using this strategy;
* __Neddleman-Wunsch Algorithm__ (DP): Computes the optimal alignment between _s1_ and _s2_. This function uses backtracking to return all optimal allignments. 

## Further Improvments

Until now, the weights for all the edit operations (insertion, deletion, mismatch and matching) are the same (except for Neddleman-Wunsch, that has -1 for all operations but mismatch and +1 for matching). Code can be added to changes these weights according to the user's needs. Neddleman's algorithm can also be improved to penalize multiple small gaps and prefer long single gaps.

Other related algorithms, such Damerau-Levenshtein or Hirschberg's can also be implemented.
