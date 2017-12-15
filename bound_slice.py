# -*- coding: utf-8 -*-
import random
import math
#A = [3, 5, 7, 6, 3]
#A = [4, 5, 5, 1, 1]
#A = [3, 5, 7, 6]
#A = [3, 5, 3, 5, 3, 8]

"""
https://codility.com/programmers/task/count_bounded_slices/
An integer K and a non-empty zero-indexed array A consisting of N integers are given.

A pair of integers (P, Q), such that 0 ≤ P ≤ Q < N, is called a slice of array A.

A bounded slice is a slice in which the difference between the maximum and minimum values in the slice is less than or equal to K. More precisely it is a slice, such that max(A[P], A[P + 1], ..., A[Q]) − min(A[P], A[P + 1], ..., A[Q]) ≤ K.

The goal is to calculate the number of bounded slices.

For example, consider K = 2 and array A such that:

    A[0] = 3
    A[1] = 5
    A[2] = 7
    A[3] = 6
    A[4] = 3
There are exactly nine bounded slices: (0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3), (4, 4).

Write a function:

def solution(K, A)

that, given an integer K and a non-empty zero-indexed array A of N integers, returns the number of bounded slices of array A.

If the number of bounded slices is greater than 1,000,000,000, the function should return 1,000,000,000.

For example, given:

    A[0] = 3
    A[1] = 5
    A[2] = 7
    A[3] = 6
    A[4] = 3
the function should return 9, as explained above.

Assume that:

N is an integer within the range [1..100,000];
K is an integer within the range [0..1,000,000,000];
each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.

Второе - их золотое, но не работает. Даже на их проверках.
"""
from measure import measure

#O(N), 90%
max_int = 1000000000
@measure
def solution1(K, A):
    count = 0
    L = len(A)
    for i in range(L):
        j = i
        mn = mx = A[i]
        current_addition = 0
        while mx - mn <= K:
            count += 1
            current_addition += 1
            if count == max_int:
                return max_int
            j += 1
            if j == L:
                count += int(((1 + (j - i)) * (j - i)) / 2) - current_addition
                if count >= max_int:
                    count = max_int
                return count
            cur = A[j]
            # Work faster than mx = max(cur, mx)
            if cur < mn: mn = cur
            if cur > mx: mx = cur
    return count

#*************************
# Their example. Mine is little faster.
maxINT = 1000000000
@measure
def solution2(K, A):
    N = len(A)

    maxQ = [0] * (N + 1)
    posmaxQ = [0] * (N + 1)
    minQ = [0] * (N + 1)
    posminQ = [0] * (N + 1)

    firstMax, lastMax = 0, -1
    firstMin, lastMin = 0, -1
    j, result = 0, 0

    for i in range(N):
        while (j < N):
            # added new maximum element
            while (lastMax >= firstMax and maxQ[lastMax] <= A[j]):
                lastMax -= 1
            lastMax += 1
            maxQ[lastMax] = A[j]
            posmaxQ[lastMax] = j
            # added new minimum element
            while (lastMin >= firstMin and minQ[lastMin] >= A[j]):
                lastMin -= 1
            lastMin += 1
            minQ[lastMin] = A[j]
            posminQ[lastMin] = j
            if (maxQ[firstMax] - minQ[firstMin] <= K):
                j += 1
            else:
                break
        result += (j - i)
        if result >= maxINT:
            return maxINT
        if posminQ[firstMin] == i:
            firstMin += 1
        if posmaxQ[firstMax] == i:
            firstMax += 1
    return result

#*********************************

"""
n1 => 1
n1, n2 => 2 + 1 = 3
n1, n2, n3 => 3 + 2 + 1 = 6
n1, n2, n3, n4 => 4 + 3 + 2 + 1 = 10
n1, n2, n3, n4, n5 => 5 + 4 + 3 + 2 + 1 = 15
"""
@measure
def solution3(K, A):
    L = len(A)
    count = 0
    for i in range(1, L):
        j = 0
        while j < L:
            cur = A[j: j + i]
            if len(cur) != i:
                break
            j += 1
            mn = min(cur)
            mx = max(cur)
            if mx - mn <= K:
                count += 1
    return count



#*************** 90%
from collections import defaultdict
max_int = 1000000000

@measure
def solution4(K, A):
    L = len(A)
    count = 0
    counters = defaultdict(int)
    tail = head = 0
    counters[A[0]] = 1
    while tail < L and head < L:
        sorted_keys = sorted(counters.keys())
        mn = sorted_keys[0]
        mx = sorted_keys[-1]
        diff = mx - mn
        if diff > K:
            start = A[tail]
            counters[start] -= 1
            if counters[start] == 0:
                del counters[start]
            tail += 1
        else:
            count += (head + 1 - tail)
            if count >= max_int:
                return max_int
            head += 1
            if head >= L:
                break
            end = A[head]
            counters[end] += 1
    return count


#****************************************
# 60%
max_int = 1000000000

@measure
def solution5(K, A):
    L = len(A)
    count = L
    results = {i:(A[i], A[i]) for i in range(L)}
    for i in range(L - 1):
        new_results = {}
        for j in results.keys():
            if j + 1 >= L:
                break
            next_value = A[j + 1]
            mn, mx = results[j]
            mn = min(next_value, mn)
            mx = max(next_value, mx)
            if abs(mx - mn) <= K:
                new_results[j + 1] = (mn, mx)
        count += len(new_results)
        if count >= max_int:
            return max_int
        results = new_results
    return count


#**************************
#90%
max_int = 1000000000
@measure
def solution6(K, A):
    L = len(A)
    count = 0
    tail = head = 0
    mn = mx = A[0]
    while tail < L and head < L:
        diff = mx - mn
        if diff > K:
            tail += 1
            mn = mx = A[tail]
            for elem in A[tail: head + 1]:
                if elem > mx: mx = elem
                if elem < mn: mn = elem
        else:
            count += (head + 1 - tail)
            if count >= max_int:
                return max_int
            head += 1
            if head >= L:
                break
            end = A[head]
            mn = min(mn, end)
            mx = max(mx, end)
    return count


#**************************

max_int = 1000000000
@measure
def solution7(K, A):
    L = len(A)
    count = 0
    tail = head = 0
    mn = mx = A[0]
    mn_position = mx_position = 0
    while tail < L and head < L:
        diff = mx - mn
        if diff > K:
            end = A[head]
            if end == mx:
                tail = mn_position + 1
            else:
                tail = mx_position + 1
            mn = mx = A[tail]
            mn_position = mx_position = tail
            current_slice = A[tail: head + 1]
            for i in range(len(current_slice) - 1, -1, -1):
                elem = current_slice[i]
                if elem >= mx:
                    mx = elem
                    mx_position = tail + i
                if elem <= mn:
                    mn = elem
                    mn_position = tail + i
                diff = mx - mn
                if diff > K:
                    tail = tail + i
                    break
        else:
            count += (head + 1 - tail)
            if count >= max_int:
                return max_int
            head += 1
            if head >= L:
                break
            end = A[head]
            if end <= mn:
                mn = end
                mn_position = head
            if end >= mx:
                mx = end
                mx_position = head
    return count

#***************************************
max_int = 1000000000

@measure
#100%!!!!!!!!!!!!!!!!
def solution8(K, A):
    L = len(A)
    count = 0
    tail = head = 0
    mn = mx = A[0]
    asc = True
    desc = True
    while tail < L and head < L:
        diff = mx - mn
        if diff > K:
            removed = A[tail]
            tail += 1
            if removed == mx:
                if asc:
                    mx = A[head]
                elif desc:
                    mx = A[tail]
                else:
                    mx = max(A[tail: head + 1])
            if removed == mn:
                if asc:
                    mn = A[tail]
                elif desc:
                    mn = A[head]
                else:
                    mn = min(A[tail: head + 1])
        else:
            count += (head + 1 - tail)
            if count >= max_int:
                return max_int
            prev_end = A[head]
            head += 1
            if head >= L:
                break
            end = A[head]
            if end < prev_end:
                asc = False
            if end > prev_end:
                desc = False
            mn = min(end, mn)
            mx = max(end, mx)

    return count


A = [5, 5, 4, 2, 4]
K = 1

s1 = solution2(K, A)
s8 = solution8(K, A)
dif = s1 - s8
if dif != 0:
    print(s1, s8)

import os
os._exit(0)

for k in range(1000):
    l = []
    N = math.ceil(random.random() * 50)
    for n in range(50):
        s = 1 #random.choice((-1, 1))
        l.append(s * math.ceil(random.random() * 50))
    s1 = solution1(N, l)
    s2 = solution2(N, l)
    s3 = solution3(N, l)
    s4 = solution4(N, l)
    s5 = solution5(N, l)
    s6 = solution6(N, l)
    s7 = solution7(N, l)
    s8 = solution8(N, l)
    dif = s2 - s8
    if dif != 0:
        print(N, l, s2, s8)


for k in range(1):
    N = 30
    l = list(range(200000))
    #random.shuffle(l)
    s1 = solution1(N, l)
    s2 = solution2(N, l)
    #s3 = solution3(N, l)
    s4 = solution4(N, l)
    #s5 = solution5(N, l)
    s6 = solution6(N, l)
    s7 = solution7(N, l)
    s8 = solution8(N, l)
    dif = s2 - s8
    if dif != 0:
        print(N, l, s2, s8)



print(measure.timers)

