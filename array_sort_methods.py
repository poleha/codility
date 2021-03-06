# -*- coding: utf-8 -*-
# https://codility.com/media/train/4-Sorting.pdf

"""
Counting sort
The idea: First, count the elements in the array of counters (see chapter 2). Next, just iterate
through the array of counters in increasing order.
Notice that we have to know the range of the sorted values. If all the elements are in the
set {0, 1, . . . , k}, then the array used for counting should be of size k + 1. The limitation here
may be available memory.

The time complexity here is O(n + k). We need additional memory O(k) to count all the
elements. At first sight, the time complexity of the above implementation may appear greater.
However, all the operations in lines 9 and 10 are performed not more than O(n) times.
"""


from measure import create_measure

timers = {}
measure = create_measure(timers)



@measure()
def simple_sort(A):
    A = A[:]
    l = len(A)
    for i in range(l - 1):
        for j in range(i + 1, l):
            left = A[i]
            right = A[j]
            if left > right:
                A[i] = right
                A[j] = left
    return A



@measure()
def counting_sort(A): # My
    counter = {}
    mn = None
    mx = None
    res = []
    for cur in A:
        counter[cur] = counter[cur] + 1 if cur in counter else 1
        if cur < mn or mn is None:
            mn = cur
        if cur > mx or mx is None:
            mx = cur

    for i in range(mn, mx + 1):
        count = counter.get(i, None)
        if count is not None:
            for j in range(count):
                res.append(i)

    return res

# Только с положительными, нужно знать разброс от минимального к максимальному. Мой метод лучше. Но питон делает быстрее )))
#@measure()
def counting_sort_examlpe(A, k):
    n = len(A)
    count = [0] * (k + 1)
    for i in xrange(n):
        count[A[i]] += 1
    p = 0
    for i in xrange(k + 1):
        for j in xrange(count[i]):
            A[p] = i
            p += 1
    return A

@measure()
def python_sort(A):
    return sorted(A)



#{'counting_sort_examlpe': 0.07371687889099121, 'counting_sort': 0.1369321346282959, 'python_sort': 0.008639097213745117}


#  Merge sort
"""
The idea: Divide the unsorted array into two halves, sort each half separately and then just
merge them. After the split, each part is halved again.
We repeat this algorithm until we end up with individual elements, which are sorted by
definition. The merging of two sorted arrays consisting of k elements takes O(k) time; just
repeatedly choose the lower of the first elements of the two merged parts.
The length of the array is halved on each iteration. In this way, we get consecutive levels
with 1, 2, 4, 8, . . . slices. For each level, the merging of the all consecutive pairs of slices requires
O(n) time. The number of levels is O(log n), so the total time complexity is O(n log n) (read
more at http://en.wikipedia.org/wiki/Merge_sort).
"""

#stud
@measure()
def merge_sort(A):

    L = len(A)
    mid = L // 2
    if L > 1:
        left = merge_sort(A[:mid])
        right = merge_sort(A[mid:])

        left_L = len(left)
        right_L = len(right)

        res = []
        left_index = 0
        right_index = 0
        while left_index < left_L and right_index < right_L:
            l = left[left_index]
            r = right[right_index]
            if l < r:
                res.append(l)
                left_index += 1
            else:
                res.append(r)
                right_index += 1
        if left_index < left_L:
            res += left[left_index:]
        if right_index < right_L:
            res += right[right_index:]

    else:
        res = A

    return res



#{'counting_sort_examlpe': 0.0036950111389160156, 'counting_sort': 0.006501197814941406, 'python_sort': 0.0004951953887939453, 'simple_sort': 33.34170198440552, 'merge_sort': 0.00534820556640625}
#print res4

from random import shuffle

A = list(range(1000)) * 3
shuffle(A)

res0 = simple_sort(A)

A = list(range(1000)) * 3
shuffle(A)

res1 = counting_sort(A)

A = list(range(1000)) * 3
shuffle(A)

res2 = counting_sort_examlpe(A, 1000)

A = list(range(1000)) * 3
shuffle(A)

res3 = python_sort(A)

A = list(range(1000)) * 3
shuffle(A)

res4 = merge_sort(A)

print(res0 == res1 == res2 == res3 == res4)
#print(res0, res1, res2, res3, res4)
print(timers)