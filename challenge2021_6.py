"""
You are given a matrix, consisting of three rows and three columns, represented as an array A of nine integers. The rows of the matrix are numbered from 0 to 2 (from top to bottom) and the columns are numbered from 0 to 2 (from left to right). The matrix element in the J-th row and K-th column corresponds to the array element A[J*3 + K]. For example, the matrix below corresponds to array [0, 2, 3, 4, 1, 1, 1, 3, 1].

[0 2 3]
       [4 1 1]
       [1 3 1]

In one move you can increment any element by 1.

Your task is to find a matrix whose elements in each row and each column sum to an equal value, which can be constructed from the given matrix in a minimal number of moves.

Write a function:

class Solution { public int[] solution(int[] A); }

that, given an array A of nine integers, returns an array of nine integers, representing the matrix described above. If there are several possible answers, the function may return any of them.

Examples:

1. Given A = [0, 2, 3, 4, 1, 1, 1, 3, 1], the function could return [1, 2, 3, 4, 1, 1, 1, 3, 2]. The sum of elements in each row and each column of the returned matrix is 6. Two increments by 1 are enough. You can increment A[0] and A[8] (top-left and bottom-right matrix elements). This gives [1, 2, 3, 4, 1, 1, 1, 3, 2], which satisfies the statement's conditions. Alternatively, you can increment A[2] and A[6] (top-right and bottom-left matrix elements). This gives another correct solution: [0, 2, 4, 4, 1, 1, 2, 3, 1].

[0 2 3]
       [4 1 1]
       [1 3 1]

[0 2 3]
       [4 1 1]
       [1 3 1]

2. Given A = [1, 1, 1, 2, 2, 1, 2, 2, 1], the function should return [1, 1, 3, 2, 2, 1, 2, 2, 1]. The sum of elements in each row and each column of the returned matrix is 5. Two increments by 1 are enough. You can increment A[2] (top-right matrix element) twice. In this case, there are no other correct solutions.

[1 1 1]
       [2 2 1]
       [2 2 1]

Write an efficient algorithm for the following assumptions:

array A contains nine elements;
each element of array A is an integer within the range [0..100,000,000].

Gold:
https://app.codility.com/cert/view/certX8UVM2-7QEP9S84UWCP7KG2/
https://app.codility.com/cert/view/certWBMTYM-U2UAGFMRNKXBW5MJ/ - BETTER
"""

def solution0(A):
    L = len(A)

    row0_inds = [0, 1, 2]
    row1_inds = [3, 4, 5]
    row2_inds = [6, 7, 8]

    col0_inds = [0, 3, 6]
    col1_inds = [1, 4, 7]
    col2_inds = [2, 5, 8]

    rows = {}
    for row in [row0_inds, row1_inds, row2_inds]:
        for e in row:
            rows[e] = row

    columns = {}
    for column in [col0_inds, col1_inds, col2_inds]:
        for e in column:
            columns[e] = column

    all_inds = [row0_inds, row1_inds, row2_inds, col0_inds, col1_inds, col2_inds]
    all_elems = []
    for inds in all_inds:
        all_elems.append([A[i] for i in inds])
    sums = [sum(e) for e in all_elems]



    print(sums)




from functools import reduce
def solution(A):
    L = len(A)

    row0_inds = [0, 1, 2]
    row1_inds = [3, 4, 5]
    row2_inds = [6, 7, 8]

    col0_inds = [0, 3, 6]
    col1_inds = [1, 4, 7]
    col2_inds = [2, 5, 8]


    all_inds = [row0_inds, row1_inds, row2_inds, col0_inds, col1_inds, col2_inds]


    rows = {}
    for row in [row0_inds, row1_inds, row2_inds]:
        for e in row:
            rows[e] = row

    columns = {}
    for column in [col0_inds, col1_inds, col2_inds]:
        for e in column:
            columns[e] = column

    def get_sums():
        all_elems = []
        for inds in all_inds:
            all_elems.append([A[i] for i in inds])
        sums = [sum(e) for e in all_elems]
        return sums


    sums = get_sums()
    if reduce(lambda a, b: a if a == b else None, sums) is not None:
        return A
    while True:
        sums = get_sums()
        max_s = max(sums)
        changed = False
        min_row_sum = float('inf')
        min_row = None
        min_column_sum = float('inf')
        min_column = None
        for i in range(L):
            row_inds = rows[i]
            column_inds = columns[i]
            row = [A[i] for i in row_inds]
            column = [A[i] for i in column_inds]
            s_row = sum(row)
            s_column = sum(column)
            if s_row < min_row_sum:
                min_row = row_inds
                min_row_sum = s_row

            if s_column < min_column_sum:
                min_column = column_inds
                min_column_sum = s_column


            if s_column == s_row:
                diff = max_s - s_row
                if diff > 0:
                    A[i] += diff
                    changed = True
        sums = get_sums()
        if reduce(lambda a, b: a if a == b else None, sums) is not None:
            break
        if not changed:
            ind = list(set(min_row).intersection(set(min_column)))[0]
            diff = int(round(max(sums) - sum(sums) / 6)) or 1
            A[ind] += diff

    return A

A = [111111111111111, 1, 1111111113, 4, 1111111111, 4, 11111111111114, 1, 1111111111112] #

# [1, 5, 3, 4, 1, 4, 4, 3, 2] - Correct
#[1, 5, 3, 4, 1, 4, 4, 3, 2]
sol = solution(A)
print(sol)