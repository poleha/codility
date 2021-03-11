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
from measure import measure


# 30% Correct but slow
# @measure
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
        return size * 2

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


@measure
def solution2(X, Y, T):
    def get_straight_point(y, line):
        line1 = [v[1] for v in line]
        next_ind = bisect.bisect(line1, y)
        try:
            y1 = line1[next_ind]
            x1 = line[next_ind][0]
            t1 = line[next_ind][2]
        except IndexError:
            return
        else:
            if y1 > y:
                if can_be_visited(y1, line):
                    return x1, y1, t1
        return

    def get_perp_lines(perp_lines_keys, x, y, straight_point, direction):
        b_stop = float('inf')

        if direction == 1:
            op = sub
        else:
            op = add

        b_start = op(y, x)
        if straight_point:
            b_stop = op(straight_point[1], straight_point[0])
        result = []
        next_b_i = bisect.bisect(perp_lines_keys, b_start)
        if next_b_i and next_b_i < len(perp_lines_keys):
            next_b = perp_lines_keys[next_b_i]
            if b_start < next_b < b_stop:
                result.extend(perp_lines_keys[next_b_i:])
        return result

    def can_be_visited(y, line):
        line1 = [v[1] for v in line]
        next_ind = bisect.bisect(line1, y)
        try:
            y1 = line1[next_ind]
        except IndexError:
            return True
        else:
            if y1 - y == 1:
                return False
        return True

    def get_possible_lines(x, y, lines_plus, lines_minus, lines_plus_keys, lines_minus_keys, direction,
                           straight_only=False):
        b_plus = y - x
        b_minus = y + x
        line_plus = lines_plus[b_plus]
        line_minus = lines_minus[b_minus]
        if direction == 1:
            straight_line = line_plus
            perp_lines_keys = lines_minus_keys
        else:
            straight_line = line_minus
            perp_lines_keys = lines_plus_keys

        straight_point = get_straight_point(y, straight_line)
        result_perp_lines = None
        if not straight_only:
            result_perp_lines = get_perp_lines(perp_lines_keys, x, y, straight_point, -direction)
        return result_perp_lines, straight_point

    def get_points(t):
        return 10 if t == 'q' else 1

    visited = {}
    points = set()
    xyt = zip(X, Y, T)
    xyt = sorted(xyt, key=lambda v: v[1])
    own_x, own_y = next((x, y) for (x, y, t) in xyt if t == 'X')
    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y]
    lines_plus = defaultdict(list)
    lines_minus = defaultdict(list)
    for x, y, t in xyt:
        points.add((x, y))
        b_plus = y - x
        b_minus = y + x
        lines_plus[b_plus].append((x, y, t))
        lines_minus[b_minus].append((x, y, t))

    lines_plus_keys = list(sorted(lines_plus.keys()))
    lines_minus_keys = list(sorted(lines_minus.keys()))

    path = []

    _, straight_point1 = get_possible_lines(own_x, own_y, lines_plus, lines_minus, lines_plus_keys, lines_minus_keys,
                                            direction=1, straight_only=True)
    _, straight_point2 = get_possible_lines(own_x, own_y, lines_plus, lines_minus, lines_plus_keys, lines_minus_keys,
                                            direction=-1,
                                            straight_only=True)

    if straight_point1:
        path.append((straight_point1[0], straight_point1[1], get_points(straight_point1[2]), 1))
        key = (straight_point1[0], straight_point1[1], 1)
        visited[key] = get_points(straight_point1[2])

    if straight_point2:
        path.append((straight_point2[0], straight_point2[1], get_points(straight_point2[2]), -1))
        key = (straight_point2[0], straight_point2[1], -1)
        visited[key] = get_points(straight_point2[2])

    while path:
        new_path = []
        for x, y, p, d in path:
            b1 = y - x if d == 1 else y + x
            perp_lines, straight_point = get_possible_lines(x, y, lines_plus, lines_minus, lines_plus_keys,
                                                            lines_minus_keys, direction=d, straight_only=False)
            if straight_point:
                current_points = p + get_points(straight_point[2])
                key = (straight_point[0], straight_point[1], d)
                visited_points = visited.get(key, 0)
                if current_points > visited_points:
                    visited[key] = current_points
                    new_path.append((straight_point[0], straight_point[1], current_points, d))
            if perp_lines:
                for b2 in perp_lines:
                    y_start = (b1 + b2) / 2
                    if y_start != round(y_start):
                        continue
                    x_start = y_start - b1 if d == 1 else b1 - y_start
                    x_start_test = b2 - y_start if d == 1 else y_start - b2
                    assert x_start == x_start_test
                    if (x_start, y_start) in points:
                        break
                    _, straight_point = get_possible_lines(x_start, y_start, lines_plus, lines_minus, lines_plus_keys,
                                                           lines_minus_keys, direction=-d, straight_only=False)
                    if straight_point:
                        current_points = p + get_points(straight_point[2])
                        key = (straight_point[0], straight_point[1], -d)
                        visited_points = visited.get(key, 0)
                        if current_points > visited_points:
                            visited[key] = current_points
                            new_path.append(
                                (straight_point[0], straight_point[1], p + get_points(straight_point[2]), -d))
        path = new_path

    try:
        result = max(visited.values())
    except ValueError:
        result = 0

    return result


from collections import defaultdict
from operator import add, sub
import bisect

@measure
def solution3(X, Y, T):
    c = {}
    def cache(func):
        def wrapper(*args, **kwargs):
            key = func.__name__ + '-'.join(str(a) for a in args) + '-'.join(f'{str(k)}:{str(v)}' for (k, v) in kwargs.items())
            value = c.get(key)
            if value is None:
                value = func(*args, **kwargs)
                c[key] = value
            return value

        return wrapper


    @cache
    def make_move(x, y, d):
        b1 = y - x if d == 1 else y + x
        perp_line_b_i, straight_point = get_possible_lines(x, y, direction=d, straight_only=False)
        if straight_point:
            b_end = straight_point[1] + straight_point[0] if d == 1 else straight_point[1] - straight_point[0]
        else:
            b_end = float('inf')

        points = 0
        if straight_point:
            current_points = get_points(straight_point[2])
            new_points = make_move(straight_point[0], straight_point[1], d) + current_points
            points = max(points, new_points)

        if perp_line_b_i is not None:
            all_perp_lines = lines_plus_keys if d == -1 else lines_minus_keys
            for b2 in all_perp_lines[perp_line_b_i:]:
                if b2 >= b_end:
                    break
                y_start = (b1 + b2) / 2
                if y_start != round(y_start):
                    continue
                x_start = y_start - b1 if d == 1 else b1 - y_start
                x_start_test = b2 - y_start if d == 1 else y_start - b2
                assert x_start == x_start_test
                if (x_start, y_start) in all_points:
                    break
                _, straight_point = get_possible_lines(x_start, y_start, direction=-d, straight_only=False)
                if straight_point:
                    current_points = get_points(straight_point[2])
                    new_points = make_move(straight_point[0], straight_point[1], -d) + current_points

                    points = max(points, new_points)
        return points

    def get_straight_point(y, b_plus, b_minus, direction):
        line_plus = lines_plus[b_plus]
        line_minus = lines_minus[b_minus]
        line_plus_y = lines_plus_y[b_plus]
        line_minus_y = lines_minus_y[b_minus]
        if direction == 1:
            line = line_plus
            line_y = line_plus_y
        else:
            line = line_minus
            line_y = line_minus_y

        next_ind = bisect.bisect(line_y, y)
        try:
            y1 = line_y[next_ind]
            x1 = line[next_ind][0]
            t1 = line[next_ind][2]
        except IndexError:
            return
        else:
            if y1 > y:
                if can_be_visited(y1, line_y):
                    return x1, y1, t1
        return

    def get_perp_lines(x, y, straight_point, direction):
        if direction == -1:
            perp_lines_keys = lines_minus_keys
        else:
            perp_lines_keys = lines_plus_keys

        b_stop = float('inf')

        if direction == 1:
            op = sub
        else:
            op = add

        b_start = op(y, x)
        if straight_point:
            b_stop = op(straight_point[1], straight_point[0])
        next_b_i = bisect.bisect(perp_lines_keys, b_start)
        if next_b_i and next_b_i < len(perp_lines_keys):
            next_b = perp_lines_keys[next_b_i]
            if b_start < next_b < b_stop:
                return next_b_i


    def can_be_visited(y, line):
        next_ind = bisect.bisect(line, y)
        try:
            y1 = line[next_ind]
        except IndexError:
            return True
        else:
            if y1 - y == 1:
                return False
        return True


    def get_possible_lines(x, y, direction, straight_only=False):
        b_plus = y - x
        b_minus = y + x

        straight_point = get_straight_point(y, b_plus, b_minus, direction)
        perp_lines_b_i = None
        if not straight_only:
            perp_lines_b_i = get_perp_lines(x, y, straight_point, -direction)
        return perp_lines_b_i, straight_point

    def get_points(t):
        return 10 if t == 'q' else 1

    all_points = set()
    xyt = zip(X, Y, T)
    xyt = sorted(xyt, key=lambda v: v[1])
    own_x, own_y = next((x, y) for (x, y, t) in xyt if t == 'X')
    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y]

    s = own_x + own_y

    own_b_plus = own_y - own_x
    own_b_minus = own_y + own_x

    def check1(x, y):
        return y >= own_b_plus + x and y >= own_b_minus - x

    def check(x, y):
        return (x + y) % 2 == s % 2

    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y and check(x, y) and check1(x, y)]

    lines_plus = defaultdict(list)
    lines_minus = defaultdict(list)
    lines_plus_y = defaultdict(list)
    lines_minus_y = defaultdict(list)

    for x, y, t in xyt:
        all_points.add((x, y))
        b_plus = y - x
        b_minus = y + x
        lines_plus[b_plus].append((x, y, t))
        lines_minus[b_minus].append((x, y, t))
        lines_plus_y[b_plus].append(y)
        lines_minus_y[b_minus].append(y)

    updated_lines_plus = defaultdict(list)
    for b, line in lines_plus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_plus[b].append(p)

    updated_lines_minus = defaultdict(list)
    for b, line in lines_minus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_minus[b].append(p)

    lines_plus = updated_lines_plus
    lines_minus = updated_lines_minus

    lines_plus_keys = list(sorted(lines_plus.keys()))
    lines_minus_keys = list(sorted(lines_minus.keys()))

    _, straight_point1 = get_possible_lines(own_x, own_y, direction=1, straight_only=True)
    _, straight_point2 = get_possible_lines(own_x, own_y, direction=-1, straight_only=True)

    if straight_point1:
        result1 = make_move(straight_point1[0], straight_point1[1], 1) + get_points(straight_point1[2])
    else:
        result1 = 0

    if straight_point2:
        result2 = make_move(straight_point2[0], straight_point2[1], -1) + get_points(straight_point2[2])
    else:
        result2 = 0
    return max(result1, result2)



from collections import defaultdict
from operator import add, sub
import bisect

@measure
def solution4(X, Y, T):
    c = {}
    def cache(func):
        def wrapper(*args, **kwargs):
            key = func.__name__ + '-'.join(str(a) for a in args) + '-'.join(f'{str(k)}:{str(v)}' for (k, v) in kwargs.items())
            value = c.get(key)
            if value is None:
                value = func(*args, **kwargs)
                c[key] = value
            return value

        return wrapper


    @cache
    def make_move(x, y, d):
        straight_point, next_points = get_possible_points(x, y, direction=d, straight_only=False)
        max_result = 0
        if straight_point:
            max_result = make_move(straight_point[0], straight_point[1], d) + get_points(straight_point[2])
        for point in next_points:
            if point[3]:
                res = make_move(point[0], point[1], -d) + get_points(point[2])
                max_result = max(res, max_result)
        return max_result

    def get_straight_point(y, b_plus, b_minus, direction):
        line_plus = lines_plus[b_plus]
        line_minus = lines_minus[b_minus]
        line_plus_y = lines_plus_y[b_plus]
        line_minus_y = lines_minus_y[b_minus]
        if direction == 1:
            line = line_plus
            line_y = line_plus_y
        else:
            line = line_minus
            line_y = line_minus_y

        next_ind = bisect.bisect(line_y, y)
        try:
            y1 = line_y[next_ind]
            x1 = line[next_ind][0]
            t1 = line[next_ind][2]
        except IndexError:
            return
        else:
            if y1 > y:
                if can_be_visited(y1, line_y):
                    return x1, y1, t1, True
                else:
                    return x1, y1, t1, False
        return


    def can_be_visited(y, line):
        next_ind = bisect.bisect(line, y)
        try:
            y1 = line[next_ind]
        except IndexError:
            return True
        else:
            if y1 - y == 1:
                return False
        return True


    def get_possible_points(x, y, direction, straight_only=False):
        b_plus = y - x
        b_minus = y + x

        next_points  = []
        real = True
        straight_point = get_straight_point(y, b_plus, b_minus, direction)
        if straight_point:
            *straight_point, real = straight_point
        if straight_only and real:
            return straight_point
        end_b = float('inf')
        if not straight_only:
            if direction > 0:
                next_points_dict = next_points_plus
                next_points_b_dict = next_points_plus_b
                b = b_plus
            else:
                next_points_dict = next_points_minus
                next_points_b_dict = next_points_minus_b
                b = b_minus
            next_points = next_points_dict[b]
            next_points_b = next_points_b_dict[b]
            start_b = b_minus if direction > 0 else b_plus
            if straight_point:
                end_b = straight_point[1] + straight_point[0] if direction > 0 else straight_point[1] - straight_point[0]


            next_points_start = bisect.bisect(next_points_b, start_b)
            next_points_end = bisect.bisect_left(next_points_b, end_b)
            #def get_b(p):
            #    return p[1] + p[0] if direction > 0 else p[1] - p[0]

            next_points = next_points[next_points_start: next_points_end]
        if not real:
            straight_point = None
        return straight_point, next_points

    def get_points(t):
        return 10 if t == 'q' else 1

    all_points = set()
    xyt = zip(X, Y, T)
    xyt = sorted(xyt, key=lambda v: v[1])
    own_x, own_y = next((x, y) for (x, y, t) in xyt if t == 'X')
    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y]

    s = own_x + own_y

    own_b_plus = own_y - own_x
    own_b_minus = own_y + own_x

    def check1(x, y):
        return y >= own_b_plus + x and y >= own_b_minus - x

    def check(x, y):
        return (x + y) % 2 == s % 2

    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y and check(x, y) and check1(x, y)]

    lines_plus = defaultdict(list)
    lines_minus = defaultdict(list)
    lines_plus_y = defaultdict(list)
    lines_minus_y = defaultdict(list)

    for x, y, t in xyt:
        all_points.add((x, y))
        b_plus = y - x
        b_minus = y + x
        lines_plus[b_plus].append((x, y, t))
        lines_minus[b_minus].append((x, y, t))
        lines_plus_y[b_plus].append(y)
        lines_minus_y[b_minus].append(y)

    updated_lines_plus = defaultdict(list)
    for b, line in lines_plus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_plus[b].append(p)

    updated_lines_minus = defaultdict(list)
    for b, line in lines_minus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_minus[b].append(p)

    lines_plus = updated_lines_plus
    lines_minus = updated_lines_minus

    next_points_plus = defaultdict(list)
    next_points_minus = defaultdict(list)

    next_points_plus_b = defaultdict(list)
    next_points_minus_b = defaultdict(list)

    for b_plus, line in lines_plus.items():
        for b_minus, perp_line in lines_minus.items():
            y = (b_plus + b_minus) / 2
            point = get_straight_point(y, b_plus, b_minus, -1)
            if point and point[-1]:
                next_points_plus[b_plus].append(point)
                next_points_plus_b[b_plus].append(b_minus)

    for b_minus, line in lines_minus.items():
        for b_plus, perp_line in lines_plus.items():
            y = (b_plus + b_minus) / 2
            point = get_straight_point(y, b_plus, b_minus, 1)
            if point and point[-1]:
                next_points_minus[b_minus].append(point)
                next_points_minus_b[b_minus].append(b_plus)


    straight_point1 = get_possible_points(own_x, own_y, direction=1, straight_only=True)
    straight_point2 = get_possible_points(own_x, own_y, direction=-1, straight_only=True)

    if straight_point1:
        result1 = make_move(straight_point1[0], straight_point1[1], 1) + get_points(straight_point1[2])
    else:
        result1 = 0

    if straight_point2:
        result2 = make_move(straight_point2[0], straight_point2[1], -1) + get_points(straight_point2[2])
    else:
        result2 = 0
    return max(result1, result2)





from collections import defaultdict
from operator import add, sub
import bisect

@measure
def solution5(X, Y, T):
    c = {}
    def cache(func):
        def wrapper(*args, **kwargs):
            key = func.__name__ + '-'.join(str(a) for a in args) + '-'.join(f'{str(k)}:{str(v)}' for (k, v) in kwargs.items())
            value = c.get(key)
            if value is None:
                value = func(*args, **kwargs)
                c[key] = value
            return value

        return wrapper


    @cache
    def make_move(x, y, d):
        straight_point, next_points = get_possible_points(x, y, direction=d, straight_only=False)
        max_result = 0
        if straight_point:
            max_result = make_move(straight_point[0], straight_point[1], d) + get_points(straight_point[2])
        for point in next_points:
            if point[3]:
                res = make_move(point[0], point[1], -d) + get_points(point[2])
                max_result = max(res, max_result)
        return max_result

    def get_straight_point(y, b_plus, b_minus, direction):
        line_plus = lines_plus[b_plus]
        line_minus = lines_minus[b_minus]
        line_plus_y = lines_plus_y[b_plus]
        line_minus_y = lines_minus_y[b_minus]
        if direction == 1:
            line = line_plus
            line_y = line_plus_y
        else:
            line = line_minus
            line_y = line_minus_y

        next_ind = bisect.bisect(line_y, y)
        try:
            y1 = line_y[next_ind]
            x1 = line[next_ind][0]
            t1 = line[next_ind][2]
        except IndexError:
            return
        else:
            if y1 > y:
                if can_be_visited(y1, line_y):
                    return x1, y1, t1, True
                else:
                    return x1, y1, t1, False
        return


    def can_be_visited(y, line):
        next_ind = bisect.bisect(line, y)
        try:
            y1 = line[next_ind]
        except IndexError:
            return True
        else:
            if y1 - y == 1:
                return False
        return True

    def can_visit(x1, y1, x2, y2):
        all_points = set()
        for d in (-1, 1):
            straight_point, next_points = get_possible_points(x1, y1, direction=d, straight_only=False)
            all_points.add(straight_point)
            all_points.update(set(next_points))
        return all_points



    def construct_maze():
        maze = defaultdict(list)
        for i in range(len(xyt)):
            for j in range(i, len(xyt)):
                x1, y1, t1 = xyt[i]
                x2, y2, t2 = xyt[j]
                left, right =  can_visit(x1, y1, y2, x2)
                if left:
                    maze[(x1, y1, -1)].append((x2, y2, left))
                if right:
                    maze[(x1, y1, 1)].append((x2, y2, right))


    def get_possible_points(x, y, direction, straight_only=False):
        b_plus = y - x
        b_minus = y + x

        next_points  = []
        real = True
        straight_point = get_straight_point(y, b_plus, b_minus, direction)
        if straight_point:
            *straight_point, real = straight_point
        if straight_only and real:
            return straight_point
        end_b = float('inf')
        if not straight_only:
            if direction > 0:
                next_points_dict = next_points_plus
                next_points_b_dict = next_points_plus_b
                b = b_plus
            else:
                next_points_dict = next_points_minus
                next_points_b_dict = next_points_minus_b
                b = b_minus
            next_points = next_points_dict[b]
            next_points_b = next_points_b_dict[b]
            start_b = b_minus if direction > 0 else b_plus
            if straight_point:
                end_b = straight_point[1] + straight_point[0] if direction > 0 else straight_point[1] - straight_point[0]


            next_points_start = bisect.bisect(next_points_b, start_b)
            next_points_end = bisect.bisect_left(next_points_b, end_b)
            #def get_b(p):
            #    return p[1] + p[0] if direction > 0 else p[1] - p[0]

            next_points = next_points[next_points_start: next_points_end]
        if not real:
            straight_point = None
        return straight_point, next_points

    def get_points(t):
        return 10 if t == 'q' else 1

    all_points = set()
    xyt = zip(X, Y, T)
    xyt = sorted(xyt, key=lambda v: v[1])
    own_x, own_y = next((x, y) for (x, y, t) in xyt if t == 'X')
    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y]

    s = own_x + own_y

    own_b_plus = own_y - own_x
    own_b_minus = own_y + own_x

    def check1(x, y):
        return y >= own_b_plus + x and y >= own_b_minus - x

    def check(x, y):
        return (x + y) % 2 == s % 2

    xyt = [(x, y, t) for (x, y, t) in xyt if y > own_y and check(x, y) and check1(x, y)]

    lines_plus = defaultdict(list)
    lines_minus = defaultdict(list)
    lines_plus_y = defaultdict(list)
    lines_minus_y = defaultdict(list)

    for x, y, t in xyt:
        all_points.add((x, y))
        b_plus = y - x
        b_minus = y + x
        lines_plus[b_plus].append((x, y, t))
        lines_minus[b_minus].append((x, y, t))
        lines_plus_y[b_plus].append(y)
        lines_minus_y[b_minus].append(y)

    updated_lines_plus = defaultdict(list)
    for b, line in lines_plus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_plus[b].append(p)

    updated_lines_minus = defaultdict(list)
    for b, line in lines_minus.items():
        for i, p in enumerate(line):
            if i > 0:
                prev_p = line[i - 1]
                if p[1] - prev_p[1] == 1:
                    continue
            updated_lines_minus[b].append(p)

    lines_plus = updated_lines_plus
    lines_minus = updated_lines_minus

    next_points_plus = defaultdict(list)
    next_points_minus = defaultdict(list)

    next_points_plus_b = defaultdict(list)
    next_points_minus_b = defaultdict(list)

    for b_plus, line in lines_plus.items():
        for b_minus, perp_line in lines_minus.items():
            y = (b_plus + b_minus) / 2
            point = get_straight_point(y, b_plus, b_minus, -1)
            if point and point[-1]:
                next_points_plus[b_plus].append(point)
                next_points_plus_b[b_plus].append(b_minus)

    for b_minus, line in lines_minus.items():
        for b_plus, perp_line in lines_plus.items():
            y = (b_plus + b_minus) / 2
            point = get_straight_point(y, b_plus, b_minus, 1)
            if point and point[-1]:
                next_points_minus[b_minus].append(point)
                next_points_minus_b[b_minus].append(b_plus)


    straight_point1 = get_possible_points(own_x, own_y, direction=1, straight_only=True)
    straight_point2 = get_possible_points(own_x, own_y, direction=-1, straight_only=True)

    if straight_point1:
        result1 = make_move(straight_point1[0], straight_point1[1], 1) + get_points(straight_point1[2])
    else:
        result1 = 0

    if straight_point2:
        result2 = make_move(straight_point2[0], straight_point2[1], -1) + get_points(straight_point2[2])
    else:
        result2 = 0
    return max(result1, result2)

values = (
    # ([-2, 0, 3, 1, 0, 3], [0, 2, 5, 7, 8, 1], "Xpppp"),
    #([3, 5, 1, 6], [1, 3, 3, 8], "Xpqp"),
     #([3, 5, 2, 6], [1, 3, 0, 8], "Xpqp"),
     #([3, 5, 1, 7], [1, 3, 3, 7], "Xppqx"),
     #([0, 6, 2, 5, 3, 0], [4, 8, 2, 3, 1, 6], 'ppqpXp'),
     #([0, 1], [2, 1], 'Xp'),
     #([0, 1, 2], [0, 1, 2], 'Xpq'),
     #([0, 2, 1], [0, 2, 19], 'Xpq'),
     #([0, 1, 2], [0, 1, 2], 'Xpp'),
    # ([0, 1, 1], [1, 0, 4], 'pXp'),
    # ([2, 0, 0], [0, 2, 4], 'Xpp'),
    # ([2, 0, 0], [0, 2, 6], 'Xpp'),
    # ([1, 0, 0], [0, 1, 1115], 'Xpp'),
     #([0, 2, 1, 1, 0, 5], [0, 2, 7, 9, 2, 5], 'Xppppp'),
    # ([0,1, 3, 6], [0, 1, 3, 6], 'Xppq'),
    # ([0, 1, 3, 6], [0, 1, 3, 6], 'Xppq'),
    # ([0, 1, 3, 4, 3], [5, 4, 2, 1, 4], 'ppqXp'),
    #([0, 3, 5, 1, 6], [4, 1, 3, 3, 8], 'pXpqp'),
    # ([1, 0, 2], [0, 1, 1], 'Xpq'),
     ([1, 5, 5, 8], [1, 3, 5, 9], 'Xppp'),
     ([3, 4, 5, 5], [2, 3, 3, 6], 'Xppp'),
     ([7, 8, 8], [1, 6, 2], 'Xpp'),
     ([0, 4, 3, 1, 2], [0, 4, 3, 1, 4], 'Xpppp'),
    # ([3, 7, 6, 4, 7, 3, 0, 0], [0, 4, 3, 1, 6, 5, 0, 5], 'Xppppppp'),
    #([5, 1, 1, 5, 3, 1, 6, 5, 10, 4, 8, 6], [0, 7, 10, 6, 7, 7, 1, 8, 11, 11, 7, 3], 'Xppppppppppp'),
    #([6, 5, 8, 8, 4, 5, 2, 9, 3, 11, 6, 5], [0, 2, 7, 6, 2, 3, 0, 11, 5, 7, 8, 5], 'Xppppppppppp'),
    ([5, 1, 2, 5, 4, 5, 6, 3, 4, 0], [3, 4, 3, 1, 0, 7, 4, 9, 9, 0], 'Xppppppppp'),

)
for X, Y, T in values:
    sol3 = solution3(X, Y, T)
    sol4 = solution4(X, Y, T)
    print(sol3, sol4)
import os
#os._exit(0)
import random

for _ in range(300):
    X = []
    Y = []
    T = ''
    for i in range(5):
        if i == 0:
            t = 'X'
        else:
            t = 'p'
        x = random.choice(range(5))
        y = random.choice(range(5))
        X.append(x)
        Y.append(y)
        T += t

    sol3 = solution3(X, Y, T)
    sol4 = solution4(X, Y, T)
    if sol3 != sol4:
        print(X, Y, T)
        print(sol3, sol4)

print(measure.timers)
