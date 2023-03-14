"""
We are given two strings P and Q, each consisting of N lowercase English letters. For each position in the strings, we have to choose one letter from either P or Q, in order to construct a new string S, such that the number of distinct letters in S is minimal. Our task is to find the number of distinct letters in the resulting string S.

For example, if P = "ca" and Q = "ab", S can be equal to: "ca", "cb", "aa" or "ab". String "aa" has only one distinct letter ('a'), so the answer is 1 (which is minimal among those strings).

Write a function:

def solution(P, Q)

that, given two strings P and Q, both of length N, returns the minimum number of distinct letters of a string S, that can be constructed from P and Q as described above.

Examples:

1. Given P = "abc", Q = "bcd", your function should return 2. All possible strings S that can be constructed are: "abc", "abd", "acc", "acd", "bbc", "bbd", "bcc", "bcd". The minimum number of distinct letters is 2, which be obtained by constructing the following strings: "acc", "bbc", "bbd", "bcc".

2. Given P = "axxz", Q = "yzwy", your function should return 2. String S must consist of at least two distinct letters in this case. We can construct S = "yxxy", where the number of distinct letters is equal to 2, and this is the only optimal solution.

3. Given P = "bacad", Q = "abada", your function should return 1. We can choose the letter 'a' in each position, so S can be equal to "aaaaa".

4. Given P = "amz", Q = "amz", your function should return 3. The input strings are identical, so the only possible S that can be constructed is "amz", and its number of distinct letters is 3.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..50,000];
strings P and Q are both of length N;
strings P and Q are made only of lowercase letters (a−z);
strings P and Q contain a total of at most 20 distinct letters.
"""
# Gold https://app.codility.com/cert/view/certXEF5J4-W9285B2AUJM246KQ/

import itertools


def solution(P, Q):
    if P == Q:
        return len(set(P))

    letters = set(P + Q)
    max_number = min(len(set(P)), len(set(Q))) + 1
    number = max_number // 2
    length = number
    visited = set()
    result = len(letters)

    pq = sorted(zip(P, Q), key=lambda e: (e[0] + e[1]), reverse=True)
    P = [e[0] for e in pq]
    Q = [e[1] for e in pq]

    while True:
        length = (length // 2) or 1
        if number in visited:
            break
        visited.add(number)
        combinations = itertools.combinations(sorted(letters), number)
        correct = True
        for combination in combinations:
            variant = set(combination)
            correct = True
            for p, q in zip(P, Q):
                if p not in variant and q not in variant:
                    correct = False
                    break
            if correct:
                result = min(result, len(variant))
                number -= length
                break
        if not correct:
            number += length

    return result


# P, Q = 'abcabcabcdnxy', 'dddeeeffffbyz'
# P, Q = 'abc', 'def'
# P, Q = 'abcdef', 'bcdefa'
# P, Q = 'loops', 'loops'
# P, Q = 'abcd', 'bcde'
# P, Q = 'abbd', 'bcde'
# P, Q = 'abcaadza', 'bcdcdeza'
P, Q = ['g', 'g', 'a', 'f', 'g', 'g', 'g', 'g', 'c'], ['c', 'c', 'g', 'g', 'g', 'd', 'f', 'd', 'g']
sol = solution(P[:], Q[:])
print(sol)
