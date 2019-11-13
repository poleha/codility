"""
You are given a matrix A consisting of N rows and M columns, where each cell contains a digit. Your task is to
find a continuous sequence of neighbouring cells, starting in the top-left corner and ending in the bottom-right
 corner (going only down and right), that creates the biggest possible integer by concatenation of digits on the path.
  By neighbouring cells we mean cells that have exactly one common side.

Write a function:

class Solution { public String solution(int[][] A); }

that, given matrix A consisting of N rows and M columns, returns a string which represents the sequence of cells
that we should pick to obtain the biggest possible integer.

For example, given the following matrix A:

[9 9 7]
       [9 7 2]
       [6 9 5]
       [9 1 2]

the function should return "997952", because you can obtain such a sequence by choosing a path as shown below:

[9 9 *]
       [* 7 *]
       [* 9 5]
       [* * 2]

Write an efficient algorithm for the following assumptions:

N and M are integers within the range [1..1,000];
each element of matrix A is an integer within the range [1..9].

"""

import random

from measure import measure

A = []
for i in range(1000):
    line = []
    for j in range(1000):
        elem = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])
        line.append(elem)
    A.append(line)


@measure
def solution1(A):
    if not A or not A[0]:
        return ''
    M = len(A)
    N = len(A[0])
    m = 10 ** (M + N - 2)
    points = [(0, 0, A[0][0] * m)]

    cache = {}
    max_value = 0
    step = 0
    while points:
        step += 1
        m = 10 ** (M + N - 2 - step)
        new_points = []
        current_max_value = 0
        for point in points:
            i, j, value = point
            key = (i, j)
            result = cache.get(key, 0)
            if result >= value:
                continue
            cache[key] = value
            if i == M - 1 and j == N - 1:
                max_value = max(value, max_value)
                continue
            if i < M - 1:
                current_value = A[i + 1][j] * m + value
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i + 1, j, current_value)
                    new_points.append(new_point)
            if j < N - 1:
                current_value = A[i][j + 1] * m + value
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i, j + 1, current_value)
                    new_points.append(new_point)

        points = [p for p in new_points if p[2] == current_max_value]
    return str(int(max_value))


@measure
def solution2(A):
    if not A or not A[0]:
        return ''
    M = len(A)
    N = len(A[0])
    points = [(0, 0, str(A[0][0]))]

    cache = {}
    max_value = '0'
    while points:
        new_points = []
        current_max_value = '0'
        for point in points:
            i, j, value = point
            key = (i, j)
            result = cache.get(key, '0')
            if result >= value:
                continue
            cache[key] = value
            if i == M - 1 and j == N - 1:
                max_value = max(value, max_value)
                continue
            if i < M - 1:
                current_value = str(A[i + 1][j])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i + 1, j, value + current_value)
                    new_points.append(new_point)
            if j < N - 1:
                current_value = str(A[i][j + 1])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i, j + 1, value + current_value)
                    new_points.append(new_point)

        points = [p for p in new_points if p[2][-1] == current_max_value]
    return max_value


@measure
def solution3(A):
    if not A or not A[0]:
        return ''
    M = len(A)
    N = len(A[0])
    points = [(0, 0, str(A[0][0]))]

    cache = {}
    max_value = '0'
    while points:
        new_points = []
        current_max_value = '0'
        for point in points:
            i, j, value = point
            key = (i, j)
            result = cache.get(key, 0)
            s = sum(int(c) for c in value)
            if result >= s:
                continue
            cache[key] = s
            if i == M - 1 and j == N - 1:
                max_value = max(value, max_value)
                continue
            if i < M - 1:
                current_value = str(A[i + 1][j])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i + 1, j, value + current_value)
                    new_points.append(new_point)
            if j < N - 1:
                current_value = str(A[i][j + 1])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i, j + 1, value + current_value)
                    new_points.append(new_point)

        points = [p for p in new_points if p[2][-1] == current_max_value]
    return max_value


# 100%
@measure
def solution4(A):
    if not A or not A[0]:
        return ''
    M = len(A)
    N = len(A[0])
    points = [(0, 0, str(A[0][0]), A[0][0])]

    cache = {}
    max_value = '0'
    while points:
        new_points = []
        current_max_value = '0'
        for point in points:
            i, j, value, s = point
            key = (i, j)
            result = cache.get(key, 0)
            if result >= s:
                continue
            cache[key] = s
            if i == M - 1 and j == N - 1:
                max_value = max(value, max_value)
                continue
            if i < M - 1:
                current_value = str(A[i + 1][j])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i + 1, j, value + current_value, s + A[i + 1][j])
                    new_points.append(new_point)
            if j < N - 1:
                current_value = str(A[i][j + 1])
                if current_value >= current_max_value:
                    current_max_value = current_value
                    new_point = (i, j + 1, value + current_value, s + A[i][j + 1])
                    new_points.append(new_point)

        points = [p for p in new_points if p[2][-1] == current_max_value]
    return max_value


sol1 = solution1(A)
print(sol1)

sol2 = solution2(A)
print(sol2)

sol3 = solution3(A)
print(sol3)

sol4 = solution4(A)
print(sol4)

print(measure.timers)
# OrderedDict([('solution1', 0.012361288070678711), ('solution2', 0.002689361572265625), ('solution3', 0.2765669822692871), ('solution4', 0.002830982208251953)])
