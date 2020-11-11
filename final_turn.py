"""
https://app.codility.com/programmers/task/final_turn/


Chin is fighting with his mortal enemy, Cho. Chin and Cho are pacifists, so their fight is actually a game of checkers on an infinite board. There are two types of pieces in checkers: pawns and queens. Chin is left with his last piece: a queen. Now it is Chin's turn − the last turn in the game.

Pieces can move only diagonally and forward. A pawn always moves one step in the up-right or up-left direction. A queen can move any number of steps in one of these two directions.

If there is a piece belonging to Cho on the line of Chin's queen's movement, Chin can beat it by leaping over it and optionally passing some more empty fields. Chin can beat only one of Cho's pieces in one move. After beating one of Cho's pieces in this way, Chin can continue his turn and make another move, but only if he can beat another piece.

Chin gains 1 point for beating a pawn and 10 points for beating a queen. Now Chin wants to know the maximum number of points he can score in a single turn. Can you help?

Write a function:

    def solution(X, Y, T)

that, given the positions of all the pieces on the board, counts the maximum number of points Chin can score in one turn. X and Y are arrays of N coordinates of pieces: an K-th piece (0 ≤ K < N) occupies board position (X[K], Y[K]); i.e. it appears in the X[K]-th column and Y[K]-th row. Each piece occupies a black field.

T is a string of N characters in which the K-th character represents the type of the K-th piece: 'p' represents one of Cho's pawns and 'q' one of Cho's queens, whilst 'X' represents Chin's queen.

For example, given:
    X = [3, 5, 1, 6]
    Y = [1, 3, 3, 8]
    T = "Xpqp"

the function should return 10. This situation is depicted in the following illustration. Chin's queen is green, Cho's pawns are checked red and her queens are plain red. The optimal turn (sequence of moves) is marked by a green path.

Given:
    X = [0, 3, 5, 1, 6]
    Y = [4, 1, 3, 3, 8]
    T = "pXpqp"

the function should return 2. Note that Chin's queen cannot jump over Cho's queen as her pawn is right behind it.

Finally, given:
    X = [0, 6, 2, 5, 3, 0]
    Y = [4, 8, 2, 3, 1, 6]
    T = "ppqpXp"

the function should return 12. Remember that the board is infinite and the queen can jump onto cells with negative coordinates.

Assume that:

        arrays X, Y and string T have the same length N;
        N is an integer within the range [1..100,000];
        each element of arrays X, Y is an integer within the range [0..100,000,000];
        no two pieces have the same coordinates;
        each piece is located on a black field (field (0, 0) is black);
        string T consists only of the following characters: "p", "q" and/or "X";
        string T contains exactly one character "X".

Complexity:

        expected worst-case time complexity is O(N*log(N));
        expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
"""

"""
           N(0)    
      NW(7)         NE(1)
           
    W(7)              E(2)
           
      SW(5)          SE(3)
            S(4)


"""


# 30% Correct but slow
def solution1(X, Y, T):
    N = len(X)
    directions = (0, 1)

    def get_field_size(X, Y, N):
        max_x = X[0]
        max_y = Y[0]
        for i in range(N):
            x = X[i]
            y = Y[i]
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        size = max(max_x, max_y)
        return size + 1

    def construct_field(X, Y, T, N):
        field = {x: {} for x in X}
        own_position = None
        for i in range(N):
            x = X[i]
            y = Y[i]
            f = T[i]
            field[x][y] = f
            if f == 'X':
                own_position = (x, y)
        return field, own_position

    def make_step(x, y, direction):
        if direction == 1:
            x1 = x + 1
            y1 = y + 1
        elif direction == 0:
            x1 = x - 1
            y1 = y + 1
        return x1, y1

    def check_coords(x, y, field):
        try:
            return field[x][y]
        except KeyError:
            return False

    def make_move(x, y, removed, points=0):
        possible_moves = []
        for direction in directions:
            x1 = x
            y1 = y
            current_removed = {}
            current_removed.update(removed)
            stop = False
            while -size <= x1 <= size and -size <= y1 <= size and not stop:
                x1, y1 = make_step(x1, y1, direction)
                point = check_coords(x1, y1, field)
                if point and point != 'X' and not check_coords(x1, y1, removed):
                    points_earned = 1 if point == 'p' else 10
                    x2, y2 = x1, y1
                    while -size <= x2 <= size and -size <= y2 <= size:
                        x2, y2 = make_step(x2, y2, direction)
                        if check_coords(x2, y2, field) and not check_coords(x2, y2, removed):
                            stop = True
                            break
                        if x not in current_removed:
                            current_removed[x] = {}
                        current_removed[x][y] = point
                        possible_moves.append((x2, y2, direction, current_removed.copy(), points + points_earned))

                elif point == 'X':
                    break

        return possible_moves

    field, own_position = construct_field(X, Y, T, N)

    size = get_field_size(X, Y, N)

    possible_moves = make_move(*own_position, removed={})
    max_points = 0
    while possible_moves:
        all_new_moves = []
        for possible_move in possible_moves:
            x, y, direction, removed, points = possible_move
            max_points = max(max_points, points)
            new_moves = make_move(x, y, removed, points)
            all_new_moves.extend(new_moves)
        possible_moves = all_new_moves

    return max_points

from collections import defaultdict
def solution2(X, Y, T):
    xy = zip(X, Y)
    xy = sorted(xy, key=lambda v:v[1], reverse=True)
    lines_plus = defaultdict(list)
    lines_minus = defaultdict(list)
    for x, y in xy:
        b_plus = y - x
        b_minus = y + x
        lines_plus[b_plus].append((x, y))
        lines_minus[b_minus].append((x, y))

    path = defaultdict(list)

    for x, y in xy:
        b_plus = y - x
        b_minus = y + x
        line_plus = lines_plus[b_plus]
        line_minus = lines_plus[b_minus]

        plus_found = False
        for x1, y1 in line_plus:
            if y1 < y:
                plus_found = True
                b_minus_stop = x1 + y1
                break
        if plus_found:
            for b_minus1 in lines_minus:
                if b_minus_stop < b_minus1 < b_minus:
                    line_minus1 = lines_minus[b_minus1]
                    for x2, y2 in line_minus1:
                        if y2 + x2 < b_minus:
                            path[(x, y)].append((x2, y2))
                            break


    print(path)
    return xy

values = (
    ([-2, 0, 3, 1, 0, 3], [0, 2, 5, 7, 8, 1], "Xpppp"),
    #([3, 5, 1, 6], [1, 3, 3, 8], "Xpqp"),
    #([0, 6, 2, 5, 3, 0], [4, 8, 2, 3, 1, 6], 'ppqpXp'),
    #([0, 1], [2, 1], 'Xp'),
    #([0, 1, 2], [0, 1, 2], 'Xpq'),
    #([0, 2, 1], [0, 2, 19], 'Xpq'),
    #([0, 1, 2], [0, 1, 2], 'Xpp'),
    #([0, 1, 1], [1, 0, 4], 'pXp'),
    #([2, 0, 0], [0, 2, 4], 'Xpp'),
    #([2, 0, 0], [0, 2, 6], 'Xpp'),
    #([1, 0, 0], [0, 1, 1115], 'Xpp'),
    #([0, 1, 1, 1], [0, 1, 9, 11], 'Xppp'),
)

for X, Y, T in values:
    sol = solution2(X, Y, T)
    print(sol)
