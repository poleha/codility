"""
You are given an N × N matrix in which every cell is colored black or white. Columns are numbered from 0 to N-1 (from left to right). This coloring is represented by a non-empty array of integers A. If the K-th number in the array is equal to X then the X lowest cells in the K-th column of the matrix are black. The rest of the cells in the K-th column are white. The task is to calculate the side length of the biggest black square (a square containing only black cells).

Write a function:

def solution(A)

that, given an array of integers A of length N representing the coloring of the matrix, returns the side length of the biggest black square.

Examples:

1. Given A = [1, 2, 5, 3, 1, 3], the function should return 2. For example, the black square of side 2 contains the two lowest rows of the 1st and 2nd columns (counting from 0).

The picture describes the first example test [1, 2, 5, 3, 1, 3].

2. Given A = [3, 3, 3, 5, 4], the function should return 3. For example, the biggest black square has side 3 and contains the three lowest rows of the last three columns.

The picture describes the second example test [3, 3, 3, 5, 4].

3. Given A = [6, 5, 5, 6, 2, 2], the function should return 4. The biggest black square has side 4 and contains the four lowest rows of the first four columns.

The picture describes the third example test [6, 5, 5, 6, 2, 2].

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
each element of array A is an integer within the range [1..N].

"""

# you can write to stdout for debugging purposes, e.g.
# print("this is a debug message")

#https://app.codility.com/cert/view/cert6B8QVY-8D7JJUS4UVC27XDV/
#https://app.codility.com/cert/view/certD54H6D-5M2JCB5B7V5WKYU5/ - эта версия лучше


from measure import measure

# Silver, correct but slow
@measure
def solution1(A):
    res = 1 if any(A) else 0
    for i in range(1, len(A)):
        cur = A[i]
        if cur <= res:
            continue
        for j in range(res, cur):
            start = max(0, i - j)
            if i - start + 1 <= res:
                break
            prob = A[start: i + 1]

            try:
                cand = min(len(prob), min(prob))
            except ValueError:
                continue
            res = max(res, cand)
    return res

@measure
def solution2(A):
    res = 1 if any(A) else 0
    if res == 0:
        return 0
    L = len(A)
    tail = 0
    head = 0
    body = [A[0]]
    current_min = A[0]
    current_len = 1
    while head <= L:
        if current_len <= current_min:
            res = max(res, current_len)
            head += 1
            try:
                cur = A[head]
            except IndexError:
                break
            body.append(cur)
            if cur < current_min:
                current_min = cur
            current_len += 1
        elif current_len > current_min:
            tail += 1
            cur = body.pop(0)
            if cur == current_min:
                current_min = min(body)
            current_len -= 1
    return res


@measure
def solution3(A):
    def find(to_find):
        length = 0
        for elem in A:
            if elem >= to_find:
                length += 1
                if length == to_find:
                    return True
            else:
                length = 0
        return False

    res = 0
    ma = max(A)
    cur = max(ma // 2, 1)
    step = cur
    visited = {cur}
    while 1 <= cur <= ma:
        step = max(step // 2, 1)
        result = find(cur)
        if result:
            res = max(res, cur)
            cur += step
        else:
            cur -= step
        if cur in visited:
            break
        visited.add(cur)
    return res


import random
"""
for i in range(100000):
    A = []
    N = 50
    for j in range(N):
        k = random.choice(range(1, N))
        #k = j + 1
        A.append(k)
    # sol1 = solution1(A)
    sol2 = solution2(A)
    sol3 = solution3(A)
    if sol2 != sol3:
        print(A)

print(measure.timers)

"""
#A = [1, 2, 5, 3, 1, 3]
#A = [3, 3, 3, 5, 4]
#A = [6, 5, 5, 6, 2, 2]
#A = [6, 5, 5, 6, 2, 2, 6, 5, 5, 6, 5]
#A = [1, 2, 3, 4, 5]
#A = [3, 4, 4, 4, 4]
#A = [3, 3]
#A = [1, 4, 2, 3, 1]
#A = [100_000] * 100_000
#A = [1, 1, 1, 1]
#A = [1, 3, 2, 4, 4, 4]
#A = [2, 1, 3, 4, 4]
#A = [7, 7, 7, 6, 6, 6, 1, 2]
A = [1]
sol = solution3(A)
print(sol)

