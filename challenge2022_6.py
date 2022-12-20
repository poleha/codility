"""
https://app.codility.com/programmers/challenges/carol_of_the_code2022/
Tom is decorating the pavement in his garden with N square tiles. Each tile is divided into four triangles of different colors (white - 'W', red - 'R', green - 'G' and blue - 'B'). A tile is described as a string of four characters denoting respectively, the color of the upper, right, bottom and left triangle. For example, the tile in the figure below is described as "WRGB".

The image illustrates an examples of tile

Tom arranged the tiles in a row and decided to rotate some of them to obtain a pretty sequence. He considers a sequence of tiles pretty if each pair of adjacent tiles shares one side of the same color.

Write a function:

def solution(A)

that, given an array A of N strings, representing the sequence of tiles, returns the minimum number of 90-degree rotations (clockwise or counter-clockwise) that Tom has to perform.

Examples:

1. Given A = ["RGBW", "GBRW"], the function should return 1.

The image illustrates the first example test.

Tom can rotate the second tile counter-clockwise once to obtain a pretty sequence.

The image illustrates the answer to the first example test.

2. Given A = ["WBGR", "WBGR", "WRGB", "WRGB", "RBGW"], the function should return 4.

The image illustrates the second example test.

Tom can obtain a pretty sequence by rotating the first and third tiles counter-clockwise and the second and fourth tiles clockwise.

The image illustrates the answer to the second example test.

3. Given A = ["RBGW", "GBRW", "RWGB", "GBRW"], the function should return 2.

The image illustrates the third example test.

Tom can rotate the first tile clockwise twice to obtain a pretty sequence.

The image illustrates the answer to the third example test.

4. Given A = ["GBRW", "RBGW", "BWGR", "BRGW"], the function should return 2.

The image illustrates the fourth example test.

Tom can rotate the first two tiles clockwise to obtain a pretty sequence.

The image illustrates the answer to the fourth example test.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
string representing a tile has 4 letters (exactly one occurrence of 'R', 'G', 'B' and 'W').
"""
#Gold
#https://app.codility.com/cert/view/certK9G8NU-A5JGZ4DCXD5F7KV2/

def move_plus(a, n):
    new_a1 = {}
    new_a2 = {}
    for ind in range(4):
        new_ind = ind + n
        if new_ind > 3:
            new_ind -= 4
        new_a1[new_ind] = a[0][ind]
        new_a2[a[0][ind]] = new_ind
    return new_a1, new_a2


def move_minus(a, n):
    new_a1 = {}
    new_a2 = {}
    for ind in range(4):
        new_ind = ind - n
        if new_ind < 0:
            new_ind += 4
        new_a1[new_ind] = a[0][ind]
        new_a2[a[0][ind]] = new_ind
    return new_a1, new_a2


def get_distance(a, b):
    a1, a2 = a
    b1, b2 = b
    left_color = a1[1]
    right_index = b2[left_color]
    dist_right = 3 - right_index
    dist_left = 1 + right_index
    if dist_left == 4:
        dist_left = 0
    if dist_right <= dist_left:
        return dist_right
    else:
        return -dist_left


def fix_elem(e):
    a1 = {}
    a2 = {}
    for i in range(4):
        v = e[i]
        a1[i] = v
        a2[v] = i
    return a1, a2


def solution(A):
    L = len(A)
    A1 = []
    for e in A:
        A1.append(fix_elem(e))
    min_total_dist = float('inf')
    for step in range(4):
        a = move_plus(A1[0], step)
        total_dist = step if step <= 2 else 1
        for i in range(1, L):
            b = A1[i]
            dist = get_distance(a, b)
            total_dist += abs(dist)
            if dist >= 0:
                f = move_plus
            else:
                f = move_minus
            a = f(b, abs(dist))
        min_total_dist = min(total_dist, min_total_dist)
    return min_total_dist


# A = ["RGBW", "GBRW"]
# A = ["WBGR", "WBGR", "WRGB", "WRGB", "RBGW"]
A = ["RBGW", "GBRW", "RWGB", "GBRW"]

sol = solution(A)
print(sol)
