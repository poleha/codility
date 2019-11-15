"""
https://app.codility.com/programmers/task/leader_slice_inc/

Integers K, M and a non-empty array A consisting of N integers, not bigger than M, are given.

The leader of the array is a value that occurs in more than half of the elements of the array, and the segment of the array is a sequence of consecutive elements of the array.

You can modify A by choosing exactly one segment of length K and increasing by 1 every element within that segment.

The goal is to find all of the numbers that may become a leader after performing exactly one array modification as described above.

Write a function:

def solution(K, M, A)

that, given integers K and M and an array A consisting of N integers, returns an array of all numbers that can become a leader, after increasing by 1 every element of exactly one segment of A of length K. The returned array should be sorted in ascending order, and if there is no number that can become a leader, you should return an empty array. Moreover, if there are multiple ways of choosing a segment to turn some number into a leader, then this particular number should appear in an output array only once.

For example, given integers K = 3, M = 5 and the following array A:

  A[0] = 2
  A[1] = 1
  A[2] = 3
  A[3] = 1
  A[4] = 2
  A[5] = 2
  A[6] = 3
the function should return [2, 3]. If we choose segment A[1], A[2], A[3] then we get the following array A:

  A[0] = 2
  A[1] = 2
  A[2] = 4
  A[3] = 2
  A[4] = 2
  A[5] = 2
  A[6] = 3
and 2 is the leader of this array. If we choose A[3], A[4], A[5] then A will appear as follows:

  A[0] = 2
  A[1] = 1
  A[2] = 3
  A[3] = 2
  A[4] = 3
  A[5] = 3
  A[6] = 3
and 3 will be the leader.

And, for example, given integers K = 4, M = 2 and the following array:

  A[0] = 1
  A[1] = 2
  A[2] = 2
  A[3] = 1
  A[4] = 2
the function should return [2, 3], because choosing a segment A[0], A[1], A[2], A[3] and A[1], A[2], A[3], A[4] turns 2 and 3 into the leaders, respectively.

Write an efficient algorithm for the following assumptions:

N and M are integers within the range [1..100,000];
K is an integer within the range [1..N];
each element of array A is an integer within the range [1..M].
"""

from collections import defaultdict


# 66%. Correct but slow.
def solution1(K, M, A):
    L = len(A)
    L1 = L / 2
    counts = defaultdict(int)
    result = set()
    for elem in A:
        counts[elem] += 1
    for start in range(L + 1 - K):
        end = start + K
        segment = A[start: end]
        new_counts = {}
        new_segment = set()
        for elem in segment:
            new_elem = elem + 1
            if elem not in new_counts:
                new_counts[elem] = counts[elem]
            if new_elem not in new_counts:
                new_counts[new_elem] = counts[new_elem]
            new_counts[elem] -= 1
            new_counts[new_elem] += 1
            new_segment.add(new_elem)
            new_segment.add(elem)
        for new_elem in new_segment:
            if new_counts[new_elem] > L1:
                result.add(new_elem)
        for elem in counts:
            if elem in new_counts:
                continue
            if counts[elem] > L1:
                result.add(elem)

    return list(sorted(result))


# 100%
def solution2(K, M, A):
    L = len(A)
    L1 = L / 2
    counts = defaultdict(int)
    result = set()
    for elem in A:
        counts[elem] += 1
    for start in range(L - K + 1):
        end = start + K
        if start == 0:
            segment = A[start: end]
            for elem in segment:
                new_elem = elem + 1
                counts[elem] -= 1
                counts[new_elem] += 1
            for elem in counts:
                if counts[elem] > L1:
                    result.add(elem)

        else:
            end -= 1
            elem_to_remove = A[start - 1]
            elem_to_add = A[end]
            if elem_to_add == elem_to_remove:
                continue
            counts[elem_to_remove] += 1
            counts[elem_to_remove + 1] -= 1
            counts[elem_to_add] -= 1
            counts[elem_to_add + 1] += 1
            # Not ideal
            for elem in {elem_to_remove, elem_to_add + 1}:
                if counts[elem] > L1:
                    result.add(elem)

    return list(sorted(result))


A = [1, 2, 3]
K = 3
M = 3

sol1 = solution1(K, M, A)
print(sol1)

sol2 = solution2(K, M, A)
print(sol2)
