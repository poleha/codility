"""
Rick is really fond of fruit juices, but he is bored of their traditional flavours. Therefore, he has decided to mix as many of them as possible to obtain something entirely new as a result.

He has N glasses, numbered from 0 to N-1, each containing a different kind of juice. The J-th glass has capacity[J] units of capacity and contains juice[J] units of juice. In each glass there is at least one unit of juice.

Rick want to create a multivitamin mix in one of the glasses. He is going to do it by pouring juice from several other glasses into the chosen one. Each of the used glasses must be empty at the end (all of the juice from each glass has to be poured out).

What is the maximum number of flavours that Rick can mix?

Write a function:

def solution(juice, capacity)

that, given arrays juice and capacity, both of size N, returns the maximum number of flavours that Rick can mix in a single glass.

Examples:

1. Given juice = [10, 2, 1, 1] and capacity = [10, 3, 2, 2], your function should return 2. Rick can pour juice from the 3rd glass into the 2nd one.

2. Given juice = [1, 2, 3, 4] and capacity = [3, 6, 4, 4], your function should return 3. Rick can pour juice from the 0th and 2nd glasses into the 1st one.

3. Given juice = [2, 3] and capacity = [3, 4], your function should return 1. No matter which glass he chooses, Rick cannot pour juice from the other one into it. The maximum number of flavours in the chosen glass is 1.

4. Given juice = [1, 1, 5] and capacity = [6, 5, 8], your function should return 3. Rick can mix all juices in the 2nd glass.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [2..100,000];
each element of arrays juice, capacity is an integer within the range [1..1,000,000,000];
arrays juice and capacity have the same length, equal to N;
for each J juice[J] ≤ capacity[J].
"""


# Silver, correct but slow, 52%
def solution1(juice, capacity):
    if not juice or not capacity:
        return 0
    if sum(juice) == 0 or sum(capacity) == 0:
        return 0

    free_spaces = [c - j for j, c in zip(juice, capacity)]
    data = zip(juice, capacity, free_spaces)
    data = sorted(data, key=lambda d: d[0])
    sorted_juices = [d[0] for d in data]
    result = 1
    for i, (*_, free_space) in enumerate(data):
        current_result = 1
        for i1, j1 in enumerate(sorted_juices):
            if i1 == i:
                continue
            current_fit = free_space - j1
            if current_fit >= 0:
                current_result += 1
                free_space = current_fit
            else:
                break
        result = max(result, current_result)
    return result


# Silver, correct but slow, 76%
def solution2(juice, capacity):
    if not juice or not capacity:
        return 0
    if sum(juice) == 0 or sum(capacity) == 0:
        return 0

    keys = [i for i in range(len(juice))]
    free_spaces = [c - j for j, c in zip(juice, capacity)]
    data = list(zip(keys, juice, free_spaces))

    data_by_juice = sorted(data, key=lambda d: d[1])
    data_by_free_space = sorted(data, key=lambda d: d[2], reverse=True)

    result = 1
    for key, j, free_space in data_by_free_space:
        current_result = 1
        for key1, j1, free_space1 in data_by_juice:
            if key == key1:
                continue
            current_fit = free_space - j1
            if current_fit >= 0:
                current_result += 1
                free_space = current_fit
            else:
                break
        if current_result >= result:
            result = current_result
        else:
            break

    return result



import bisect
from collections import defaultdict

# Gold. 100%
def solution4(juice, capacity):
    if not juice or not capacity:
        return 0
    if sum(juice) == 0 or sum(capacity) == 0:
        return 0

    keys = [i for i in range(len(juice))]
    free_spaces = [c - j for j, c in zip(juice, capacity)]
    data = list(zip(keys, juice, free_spaces))

    data_by_juice = sorted(data, key=lambda d: d[1])
    data_by_free_space = sorted(data, key=lambda d: d[2], reverse=True)
    sorted_juice_keys = [d[0] for d in data_by_juice]

    result = 1
    sums = []
    for i, (key1, j1, free_space1) in enumerate(data_by_juice):
        if i == 0:
            sums.append(j1)
        else:
            sums.append(sums[i - 1] + j1)

    visiteds = {}
    for key, j, free_space in data_by_free_space:
        sum_index = bisect.bisect(sums, free_space) - 1
        s = sums[sum_index]
        try:
            s1 = sums[sum_index + 1]
        except IndexError:
            s1 = None
        if sum_index in visiteds:
            visited_keys = visiteds[sum_index]
        else:
            visited_keys = set(sorted_juice_keys[:sum_index + 1])
            visiteds[sum_index] = visited_keys

        count = count1 = sum_index + 2

        if key in visited_keys:
            elem_to_remove = juice[key]
            s -= elem_to_remove
            count -= 1
            if s1:
                s1 -= elem_to_remove
        if s1 and s1 <= free_space:
            if count1 >= result:
                result = count1
            else:
                break
        elif s <= free_space:
            if count >= result:
                result = count
            else:
                break

    return result


# juice = [10, 2, 1, 1]
# capacity = [10, 3, 2, 2]

# juice =    [1, 2, 3, 4]
# capacity = [3, 6, 4, 4]

juice = [1, 1, 5]
capacity = [6, 5, 8]

# juice = [2, 3]
# capacity = [3, 4]

# juice =    [5, 6, 6, 5, 3]
# capacity = [8, 10, 9, 8, 7]

# juice =    [1, 2, 3, 4]
# capacity = [3, 6, 4, 4]

juice = [1, 2]
capacity = [4, 3]

juice = [1, 2, 5]
capacity = [9, 3, 6]

sol = solution4(juice, capacity)
print(sol)

"""
Наверное достаточно проверить два варианта.
1) Максимум free space при максимальном juice. Получим N
2) Взять сумму N первых и посмотреть, влезают ли они

Или... 
Если идти по juices отсортированным. Сумма. Влезает?
"""
