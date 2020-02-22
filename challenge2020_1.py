"""
There are N rectangular buildings standing along the road next to each other. The K-th building is of size H[K] × 1.

Because a renovation of all of the buildings is planned, we want to cover them with rectangular banners until the renovations are finished. Of course, to cover a building, the banner has to be at least as high as the building. We can cover more than one building with a banner if it is wider than 1.

For example, to cover buildings of heights 3, 1, 4 we could use a banner of size 4×3 (i.e. of height 4 and width 3), marked here in blue:

Buildings of sizes (3 × 1), (1 × 1), (4 × 1), covered with scaffolding of size 4×3

We can order at most two banners and we want to cover all of the buildings. Also, we want to minimize the amount of material needed to produce the banners.

What is the minimum total area of at most two banners which cover all of the buildings?

Write a function:

def solution(H)

that, given an array H consisting of N integers, returns the minimum total area of at most two banners that we will have to order.

Examples:

1. Given H = [3, 1, 4], the function should return 10. The result can be achieved by covering the first two buildings with a banner of size 3×2 and the third building with a banner of size 4×1:

Illustration of first example

2. Given H = [5, 3, 2, 4], the function should return 17. The result can be achieved by covering the first building with a banner of size 5×1 and the other buildings with a banner of size 4×3:

Illustration of second example

3. Given H = [5, 3, 5, 2, 1], your function should return 19. The result can be achieved by covering the first three buildings with a banner of size 5×3 and the other two with a banner of size 2×2:

Illustration of third example

4. Given H = [7, 7, 3, 7, 7], your function should return 35. The result can be achieved by using one banner of size 7×5:

Illustration of fourth example

5. Given H = [1, 1, 7, 6, 6, 6], your function should return 30. The result can be achieved by using banners of size 1×2 and 7×4:

Illustration of fifth example

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
each element of array H is an integer within the range [1..10,000].
"""

from operator import gt, ge


def solution(H):
    L = len(H)
    if sum(H) / L == H[0]:
        return H[0] * L

    min_size = float('inf')

    for j in range(2):
        max_height = 0
        max_index = None
        max_height_left = 0
        max_height_right = 0
        if j == 0:
            op = ge
        else:
            op = gt
        for i, e in enumerate(H):
            if op(e, max_height):
                max_height = e
                max_index = i

        for i in range(max_index):
            e = H[i]
            if e > max_height_left:
                max_height_left = e

        for i in range(max_index + 1, L):
            e = H[i]
            if e > max_height_right:
                max_height_right = e

        len_left = max_index
        len_right = L - max_index - 1

        option1 = len_left * max_height_left + (len_right + 1) * max_height
        option2 = len_right * max_height_right + (len_left + 1) * max_height

        min_size = min([option1, option2, min_size])
    return min_size


example = [2, 3, 2, 1, 1, 1, 1, 1]
sol = solution(example)
print(sol)
