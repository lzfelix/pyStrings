# pyStrings

A repository containing some Dynamic Programming String algorithms. For now the following methods were implemented:

* __Levenshtein distance__ (recursive);
* __Levenshtein distance__ (DP): Includes showing which operations should be performed to transform string_1 into string_2;
* __Levenshtein shortened version__ (DP): Keeps in memory just 2 lines of the matrix, with length min{len(string_1), len(string_2)}, differently from the original implementation that has space complexity O(len(s1)*len(s2). On the other hand, when this method is used, it is impossible to know which operations should be performed to transform one
string into another.
