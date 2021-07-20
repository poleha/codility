"""
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

# TODO Not solved!
from measure import measure

def solution1(N, K, A, B, C):
    cakes = [[] for _ in range(N)]
    for i, (a, b, c) in enumerate(zip(A, B, C)):
        for j in range(a - 1, b):
            cakes[j].append(c)
    count = 0
    for cake in cakes:
        
        L = len(cake)
        
        if L != K:
            continue
        correct = True
        for i in range(1, L):
            prev = cake[i - 1]
            cur = cake[i]
            if cur - prev != 1:
                correct = False
                break
        if correct:
            count += 1
    
    return count


def solution2(N, K, A, B, C):
    cakes = {i + 1: [] for i in range(N)}
    for a, b, c in zip(A, B, C):
        for cake_number, cake in list(cakes.items()):
            if a <= cake_number <= b:
                if cake:
                    prev_c = cake[-1]
                    if c - prev_c != 1 or len(cake) == K:
                        del cakes[cake_number]
                        continue
                else:
                    if c != 1:
                        del cakes[cake_number]
                        continue

                cake.append(c)
                if len(cake) > K:
                    del cakes[cake_number]

    cakes = [1 for c in cakes.values() if len(c) == K]
    return len(cakes)

def solution3(N, K, A, B, C):
    abc = zip(A, B, C, range(len(A)))
    abc = sorted(abc, key=lambda e: (e[0], e[-1]))
    result = 0
    currents = []
    i = 0
    for platform in range(1, N + 1):
        while True:
            try:
                a, b, c, ind = abc[i]
            except IndexError:
                break
            if a > platform:
                break
            currents.append((a, b, c, ind))
            i += 1
        currents = sorted(currents, key=lambda e: e[-1])
        new_currents = []
        prev_c = None
        number = 0
        correct = True
        for a0, b0, c0, ind0 in currents:
            number += 1
            if not a0 <= platform or not b0 >= platform:
                continue
            new_currents.append((a0, b0, c0, ind0))
            if prev_c and c0 - prev_c != 1:
                correct = False
            prev_c = c0
        currents = new_currents
        if correct and len(new_currents) == K:
            result += 1
    return result


# Fastest so far
from collections import defaultdict
@measure
def solution4(N, K, A, B, C):
    abc = zip(A, B, C, range(len(A)))
    starts = defaultdict(list)
    ends = defaultdict(list)
    result = 0
    for a, b, c, i in abc:
        starts[a].append(i)
        ends[b].append(i)
    items = []
    for cake in range(1, N + 1):
        start_items = starts[cake]
        if cake > 1:
            end_items = set(ends[cake - 1])
        else:
            end_items = set()
        items = sorted([e for e in (items + start_items) if e not in end_items])
        if len(items) != K:
            continue
        prev_color = None
        correct = True
        for item in items:
            color = C[item]
            if prev_color and color - prev_color != 1:
                correct = False
                break
            prev_color = color
        if correct:
            result += 1

    return result


def solution5(N, K, A, B, C):
    result = 0
    abc = zip(A, B, C, range(len(A)))
    abc = sorted(abc, key=lambda e: (e[1]), reverse=True)
    for cake_number in range(1, N + 1):
        cake_inds = []
        for a, b, c, ind in abc:
            if cake_number > b:
                break
            if cake_number >= a:
                cake_inds.append(ind)
                if len(cake_inds) > K:
                    break
        if len(cake_inds) == K:
            cake_inds = sorted(cake_inds)
            cake_colors = [C[i] for i in cake_inds]
            correct = True
            for i in range(1, len(cake_colors)):
                cur = cake_colors[i]
                prev = cake_colors[i - 1]
                if cur - prev != 1:
                    correct = False
                    break
            if correct:
                result += 1
    return result


from collections import defaultdict
import bisect
@measure
def solution10(N, K, A, B, C):
    cakes = {i + 1: [] for i in range(N)}
    cake_keys = range(1, N + 1)
    for a, b, c in zip(A, B, C):
        start_cake_ind = bisect.bisect_left(cake_keys, a)
        to_remove = set()
        for cake_number in cake_keys[start_cake_ind:]:
            if cake_number > b:
                break
            cake = cakes[cake_number]
            if cake:
                prev_c = cake[-1]
                if c - prev_c != 1 or len(cake) == K:
                    del cakes[cake_number]
                    to_remove.add(cake_number)
                    continue
            else:
                if c != 1:
                    del cakes[cake_number]
                    to_remove.add(cake_number)
                    continue
            cake.append(c)
            if len(cake) > K:
                del cakes[cake_number]
                to_remove.add(cake_number)

        if to_remove:
            new_cake_keys = []
            for key in cake_keys:
                if key not in to_remove:
                    new_cake_keys.append(key)
            cake_keys = new_cake_keys

    cakes = [1 for c in cakes.values() if len(c) == K]
    return len(cakes)


# Think fastest so far
import bisect
from collections import defaultdict
@measure
def solution12(N, K, A, B, C):
    colors = sorted(set(C))
    start_set = set(colors[:-K + 1])
    abc = zip(A, B, C, range(len(A)))
    starts = defaultdict(set)
    ends = defaultdict(set)
    result = 0
    for a, b, c, i in abc:
        starts[a].add(i)
        ends[b].add(i)
    items = []
    prev_result = None
    for cake in range(1, N + 1):
        start_items = starts[cake]
        if cake > 1:
            end_items = ends[cake - 1]
        else:
            end_items = set()
        if not start_items and not end_items and prev_result is not None:
            if prev_result:
                result += 1
            continue
        for item in start_items:
            bisect.insort_right(items, item)
        if end_items:
            new_items = []
            for item in items:
                if item not in end_items:
                    new_items.append(item)
            items = new_items
        if len(items) == K and C[items[0]] in start_set:
            prev_color = None
            correct = True
            for item in items:
                color = C[item]
                if prev_color and color - prev_color != 1:
                    correct = False
                    break
                prev_color = color
            if correct:
                result += 1
                prev_result = True
            else:
                prev_result = False
        else:
            prev_result = False

    return result


from collections import defaultdict
import bisect
@measure
def solutionZX(N, K, A, B, C):
    colors = sorted(set(C))
    combs = []
    for i in range(K):
        comb = colors[i:][:K]
        if len(comb) == K:
            combs.append(comb)
    for comb in combs:
        current_comb = []
        current_cakes = []
        for i, (a, b, c) in enumerate(zip(A, B, C)):
            print(a, b, c, i)


from collections import defaultdict
@measure
def solutionWDD(N, K, A, B, C):
    abc = zip(A, B, C, range(len(A)))
    starts = defaultdict(set)
    ends = defaultdict(set)
    result = 0
    for a, b, c, i in abc:
        starts[a].add(i)
        ends[b].add(i)
    items = set()
    corrects = {}
    for cake in range(1, N + 1):
        start_items = starts[cake]
        if cake > 1:
            end_items = ends[cake - 1]
        else:
            end_items = set()

        if not start_items and not end_items and cake > 1:
            res = corrects[cake - 1]
            if res:
                result += 1
                corrects[cake] = True
                continue
            else:
                corrects[cake] = False
                continue

        if start_items:
            items.update(start_items)
        if end_items:
            items -= end_items
        if len(items) == K:
            min_item = min(items)
            max_item = max(items)
            if max_item < min_item:
                corrects[cake] = False
                continue

            min_color = C[min_item]
            max_color = C[max_item]
            if max_color - min_color == K - 1:
                correct = True
                sorted_items = sorted(items)
                colors = (C[i] for i in sorted_items)
                prev_color = None
                for color in colors:
                    if prev_color and color - prev_color != 1:
                        correct = False
                        break
                if correct:
                    corrects[cake] = True
                    result += 1
                else:
                    corrects[cake] = False
        else:
            corrects[cake] = False
    return result

#не работает
def solutionGRGF(N, K, A, B, C):
    result = 0
    cakes = {0: set(range(1, N + 1))}
    starts = {}
    failed = set()
    for a, b, c in zip(A, B, C):
        key = c - 1
        damaged1 = set()
        damaged2 = set()
        updated = False
        s = set(range(a, b + 1))
        zeros = cakes[0]
        if zeros:
            replacements = zeros.intersection(s) - failed
            damaged1 = s - replacements
            if replacements:
                updated = True
            for replacement in replacements:
                starts[replacement] = c
            if c not in cakes:
                cakes[c] = set()
            cakes[c].update(replacements)
            zeros -= replacements


        if key != 0:
            prevs = cakes.get(key)
            if prevs:
                replacements = prevs.intersection(s) - failed
                damaged2 = s - replacements
                if replacements:
                    updated = True
                if c not in cakes:
                    cakes[c] = set()
                cakes[c].update(replacements)
                prevs -= replacements
        if not updated:
            failed.update(s)
        else:
            damaged = damaged1.intersection(damaged2)
            failed.update(damaged)
    for cake, start_color in starts.items():
        if cake not in failed:
            desired_color = K - start_color + 1
            if cake in cakes.get(desired_color, set()):
                result += 1
    return result

# не всегда работает + медленно
def solutionАВА(N, K, A, B, C):
    cakes = [[] for _ in range(1, N + 2)]
    failed = set()
    for a, b, c in zip(A, B, C):
        for j in (e for e in range(a, b + 1) if e not in failed):
            cake = cakes[j]
            if cake:
                prev_color = cake[2]
                if c - prev_color == 1 and cake[0] + 1 <= K and cakes[1]:
                    cake = (cake[0] + 1, True, c)
                else:
                    cake = (cake[0] + 1, False, c)
                    failed.add(j)
                cakes[j] = cake
            else:
                cakes[j] = (1, True, c)

    return len([c for c in cakes if c and c[0] == K and c[1]])

# Correct but slow and doesn't fit into memory
def solutionWDW(N, K, A, B, C):
    L = len(C)
    res = 0
    factory = []
    for i in range(L):
        layer = [0 for _ in range(N)]
        factory.append(layer)
    for i, (a, b, c) in enumerate(zip(A, B, C)):
        factory[i][a - 1: b] = (c for _ in range(a - 1, b))
    for cake in range(N):
        prev = None
        correct = True
        count = 0
        for layer in range(L):
            cur = factory[layer][cake]
            if not cur:
                continue
            count += 1
            if count > K:
                correct = False
                break
            if prev:
                if cur - prev != 1:
                    correct = False
                    break
            prev = cur
        if correct and count == K:
            res += 1
    return res

from collections import defaultdict
import bisect
@measure
def solution(N, K, A, B, C):
    abc = zip(A, B, C, range(len(A)))
    starts = defaultdict(set)
    ends = defaultdict(set)
    result = 0
    for a, b, c, i in abc:
        starts[a].add(i)
        ends[b].add(i)
    items = []
    prev_result = None
    for cake in range(1, N + 1):
        start_items = starts[cake]
        if cake > 1:
            end_items = ends[cake - 1]
        else:
            end_items = set()
        if not start_items and not end_items and prev_result is not None:
            if prev_result:
                result += 1
            continue
        for item in start_items:
            bisect.insort_right(items, item)
        if end_items:
            new_items = []
            for item in items:
                if item not in end_items:
                    new_items.append(item)
            items = new_items
        L = len(items)
        if L == K:
            prev_color = None
            correct = True
            for i, item in enumerate(items):
                if i >= L // 2:
                    break
                color = C[item]
                sym_color = C[items[-(i + 1)]]
                if sym_color - color != (K - 1) - i * 2:
                    correct = False
                    break
                if prev_color and color - prev_color != 1:
                    correct = False
                    break
                prev_color = color
            if correct:
                result += 1
                prev_result = True
            else:
                prev_result = False
        else:
            prev_result = False

    return result

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
#N, K, A, B, C = (1, 1, [1], [1], [1])
#sol = solution(N, K, A, B, C)
#print(sol)


sol = solution(N, K, A, B, C)
sol1 = solution4(N, K, A, B, C)
if sol1 != sol:
    print(sol1, sol)
print(measure.timers)
import random
raise Exception


for _ in range(1):
    #N = random.randint(1, 500_000)
    #K = random.randint(5, 1500)
    #M = random.randint(1, 500_000)
    #A = []
    #B = []
    #C = []
    #for i in range(1, M):
    #    a = random.randint(1, N)
    #    b = random.randint(a, N)
    #    c = random.randint(1, K)
    #    A.append(a)
    #    B.append(b)
    #    C.append(c)


    M = 100_000
    N = 100_000
    K = 50_000
    A = list(range(1, M))
    B = [M] * M
    C = list(range(M))
    #N, K, A, B, C = (6, 4, [1, 2, 1, 1], [3, 3, 6, 6], [1, 2, 3, 4])
    #N, K, A, B, C = (1, 1, [1], [1], [1])
    sol = solution(N, K, A, B, C)
    sol1 = solution(N, K, A, B, C)
    if sol1 != sol:
        print(sol1, sol)



    #N, K, A, B, C = (3, 2, [1, 3, 3, 1, 1], [2, 3, 3, 1, 2], [1, 2, 1, 2, 2])
    #sol = solution(N, K, A, B, C)
    #print(sol)


print(measure.timers)