"""
https://app.codility.com/programmers/task/cake_factory/
There is a cake factory producing K-flavored cakes. Flavors are numbered from 1 to K.
A cake should consist of exactly K layers, each of a different flavor.
 It is very important that every flavor appears in exactly one cake layer and that the flavor
  layers are ordered from 1 to K from bottom to top. Otherwise the cake doesn't
  taste good enough to be sold. For example, for K = 3, cake [1, 2, 3] is well-prepared and
  can be sold, whereas cakes [1, 3, 2] and [1, 2, 3, 3] are not well-prepared.

The factory has N cake forms arranged in a row, numbered from 1 to N.
Initially, all forms are empty. At the beginning of the day a machine for producing cakes
executes a sequence of M instructions (numbered from 0 to M−1) one by one.
The J-th instruction adds a layer of flavor C[J] to all forms from A[J] to B[J], inclusive.

What is the number of well-prepared cakes after executing the sequence of M instructions?

Write a function:

def solution(N, K, A, B, C)

that, given two integers N and K and three arrays of integers A, B, C describing the sequence, returns the number of well-prepared cakes after executing the sequence of instructions.

Examples:

1. Given N = 5, K = 3, A = [1, 1, 4, 1, 4], B = [5, 2, 5, 5, 4] and C = [1, 2, 2, 3, 3].

There is a sequence of five instructions:

The 0th instruction puts a layer of flavor 1 in all forms from 1 to 5.
The 1st instruction puts a layer of flavor 2 in all forms from 1 to 2.
The 2nd instruction puts a layer of flavor 2 in all forms from 4 to 5.
The 3rd instruction puts a layer of flavor 3 in all forms from 1 to 5.
The 4th instruction puts a layer of flavor 3 in the 4th form.
The picture describes the first example test.

The function should return 3. The cake in form 3 is missing flavor 2, and the cake in form 5 has additional flavor 3. The well-prepared cakes are forms 1, 2 and 5.

2. Given N = 6, K = 4, A = [1, 2, 1, 1], B = [3, 3, 6, 6] and C = [1, 2, 3, 4],

The picture describes the second example test.

the function should return 2. The 2nd and 3rd cakes are well-prepared.

3. Given N = 3, K = 2, A = [1, 3, 3, 1, 1], B = [2, 3, 3, 1, 2] and C = [1, 2, 1, 2, 2],

The picture describes the third example test.

the function should return 1. Only the 2nd cake is well-prepared.

4. Given N = 5, K = 2, A = [1, 1, 2], B = [5, 5, 3] and C = [1, 2, 1],

The picture describes the fourth example test.

the function should return 3. The 1st, 4th and 5th cakes are well-prepared.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
M is an integer within the range [1..200,000];
each element of arrays A, B is an integer within the range [1..N];
each element of array C is an integer within the range [1..K];
for every integer J, A[J] ≤ B[J];
arrays A, B and C have the same length, equal to M.
"""

"""
N - форм
K - вкусов
A - B start - end
C = вкус
"""
from measure import measure

from collections import defaultdict
import bisect
@measure
def solution(N, K, A, B, C):
    abc = zip(A, B, C, range(len(A)))
    elems = {i: C[i] for i in range(len(A))}

    def get_initial_data():
        starts = defaultdict(list)
        ends = defaultdict(list)
        for a, b, c, i in abc:
            starts[a].append(i)
            ends[b].append(i)
        return starts, ends

    starts, ends = get_initial_data()

    def get_result():
        result = 0
        colors = []
        items = []
        count = 0
        errors_left = {}
        errors_right = {}
        error_count = 0

        prev_correct = False
        for cake in range(1, N + 1):
            start_items = starts[cake]
            if cake > 1:
                end_items = ends[cake - 1]
            else:
                end_items = []

            if not start_items and not end_items:
                if prev_correct:
                    result += 1
                continue

            if len(end_items) != count:
                for end_i in end_items:
                    ind = bisect.bisect_left(items, end_i)

                    left_ind = ind - 1
                    current_ind = ind
                    right_ind = ind + 1

                    if current_ind > 0:
                        left_item = items[left_ind]
                        left_color = colors[left_ind]
                    else:
                        left_item = None
                        left_color = None

                    current_item = end_i

                    # current
                    saved_right_error = errors_right.get(current_item, True)
                    saved_left_error = errors_left.get(current_item, True)
                    if not saved_right_error:
                        errors_right[current_item] = True
                        error_count -= 1

                    if not saved_left_error:
                        errors_left[current_item] = True
                        error_count -= 1

                    try:
                        right_item = items[right_ind]
                        right_color = colors[right_ind]
                    except IndexError:
                        right_item = None
                        right_color = None

                    # left and right
                    saved_right_error = errors_right.get(left_item, True)
                    saved_left_error = errors_left.get(right_item, True)

                    if left_item is not None and right_item is not None:
                        if left_color < right_color:
                            if not saved_right_error:
                                error_count -= 1
                            if not saved_left_error:
                                error_count -= 1
                            errors_right[left_item] = True
                            errors_left[right_item] = True

                        else:
                            if saved_right_error:
                                error_count += 1
                            if saved_left_error:
                                error_count += 1
                            errors_right[left_item] = False
                            errors_left[right_item] = False
                    elif left_item is not None and right_item is None:
                        if not saved_right_error:
                            error_count -= 1
                        errors_right[left_item] = True

                    elif right_item is not None and left_item is None:
                        if not saved_left_error:
                            error_count -= 1
                        errors_left[right_item] = True

                    items.pop(ind)
                    colors.pop(ind)
                    count -= 1
            else:
                colors = []
                items = []
                count = 0
                errors_left = {}
                errors_right = {}
                error_count = 0

            for start_i in start_items:
                c = elems[start_i]
                ind = bisect.bisect_left(items, start_i)
                items.insert(ind, start_i)
                colors.insert(ind, c)
                count += 1

                left_ind = ind - 1
                current_ind = ind
                right_ind = ind + 1

                if current_ind > 0:
                    left_item = items[left_ind]
                    left_color = colors[left_ind]
                else:
                    left_item = None
                    left_color = None

                current_item = start_i

                try:
                    right_item = items[right_ind]
                    right_color = colors[right_ind]
                except IndexError:
                    right_item = None
                    right_color = None

                # left and cur
                saved_right_error = errors_right.get(left_item, True)
                saved_left_error = errors_left.get(current_item, True)

                if left_item is not None:
                    if left_color < c:
                        if not saved_right_error:
                            error_count -= 1
                        if not saved_left_error:
                            error_count -= 1
                        errors_right[left_item] = True
                        errors_left[current_item] = True

                    else:
                        if saved_right_error:
                            error_count += 1
                        if saved_left_error:
                            error_count += 1
                        errors_right[left_item] = False
                        errors_left[current_item] = False
                else:
                    if not saved_left_error:
                        error_count -= 1
                    errors_left[current_item] = True
                # cur and right

                saved_right_error = errors_right.get(current_item, True)
                saved_left_error = errors_left.get(right_item, True)

                if right_item is not None:
                    if c < right_color:
                        if not saved_right_error:
                            error_count -= 1
                        if not saved_left_error:
                            error_count -= 1
                        errors_right[current_item] = True
                        errors_left[right_item] = True

                    else:
                        if saved_right_error:
                            error_count += 1
                        if saved_left_error:
                            error_count += 1
                        errors_right[current_item] = False
                        errors_left[right_item] = False
                else:
                    if not saved_right_error:
                        error_count -= 1
                    errors_right[current_item] = True

            if count == K and error_count == 0:
                result += 1
                prev_correct = True
            else:
                prev_correct = False

        return result
    return get_result()


import random
N = 100_000
K = 100_000
A = [1] * N
B = [random.randint(1, 1000) for _ in range(N)]
C = range(1, N + 1)

#N, K, A, B, C = (1, 1, [1], [1], [1])
#N, K, A, B, C =  (3, 1, [1, 2], [2, 3], [1, 1])
#N, K, A, B, C = (6, 4, [1, 2, 1, 1], [3, 3, 6, 6], [1, 2, 3, 4])
#N, K, A, B, C = (3, 2, [1, 3, 3, 1, 1], [2, 3, 3, 1, 2], [1, 2, 1, 2, 2])
#N, K, A, B, C = (5, 3, [1, 1, 4, 1, 4], [5, 2, 5, 5, 4], [1, 2, 2, 3, 3])
N, K, A, B, C = (3, 1, [1, 2], [2, 3], [1, 1])

#N, K, A, B, C = (1, 1, [1], [1], [1])
#sol = solution(N, K, A, B, C)
#print(sol)
#N, K, A, B, C = (3, 5, [2, 2, 3, 3, 1, 2], [3, 3, 3, 3, 1, 3], [4, 3, 5, 1, 3, 2])
#N, K, A, B, C = (6, 5, [2, 4, 5, 3, 3, 5, 1], [6, 5, 6, 4, 5, 5, 6], [1, 2, 1, 3, 4, 4, 5])
#N, K, A, B, C = 7, 5, [1, 1, 6, 3, 3, 2, 3], [7, 2, 6, 4, 5, 6, 6], [3, 1, 2, 4, 1, 2, 5]
#N, K, A, B, C = 2, 5, [1, 1, 1, 1, 1, 1], [2, 2, 1, 2, 2, 2], [1, 2, 1, 3, 4, 5]
#N, K, A, B, C = 7, 5, [6, 7, 2, 2, 5, 6, 5], [7, 7, 7, 6, 7, 6, 7], [1, 2, 3, 5, 4, 5, 5]
N, K, A, B, C = 30, 3, [18, 17, 25, 10, 1, 6, 1, 2, 28, 21, 30, 25, 25, 16, 13, 5, 1, 7, 4, 7], [18, 17, 26, 24, 10, 21, 28, 4, 28, 26, 30, 28, 26, 26, 29, 22, 2, 25, 15, 8], [2, 1, 1, 3, 1, 2, 1, 2, 2, 3, 2, 2, 3, 1, 3, 3, 2, 1, 2, 1]


sol = solution(N, K, A, B, C)
sol1 = solution(N, K, A, B, C)
if sol1 != sol:
    print(sol1, sol)
print(measure.timers)
import random
#raise Exception


for _ in range(100):
    N = random.randint(1, 55)
    K = random.randint(3, 100)
    M = random.randint(1, 80)
    A = []
    B = []
    C = []
    for i in range(1, M):
        a = random.randint(1, N)
        b = random.randint(a, N)
        c = random.randint(1, K)
        A.append(a)
        B.append(b)
        C.append(c)


    #M = 100_000
    #N = 100_000
    #K = 50_000
    #A = list(range(1, M))
    #B = [M] * M
    #C = list(range(M))
    #N, K, A, B, C = (6, 4, [1, 2, 1, 1], [3, 3, 6, 6], [1, 2, 3, 4])
    #N, K, A, B, C = (1, 1, [1], [1], [1])
    sol = 0
    if sol > 0:
        k = 1
    else:
        k = 1
    for _ in range(k):
        sol = solution(N, K, A, B, C)
        sol1 = solution(N, K, A, B, C)
        if sol1 != sol:
            print(N, K, A, B, C)
            print(sol1, sol)



    #N, K, A, B, C = (3, 2, [1, 3, 3, 1, 1], [2, 3, 3, 1, 2], [1, 2, 1, 2, 2])
    #sol = solution(N, K, A, B, C)
    #print(sol)


print(measure.timers)