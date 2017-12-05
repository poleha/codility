# -*- coding: utf-8 -*-
"""
A bracket sequence is considered to be a valid bracket expression if any of the following conditions is true:

it is empty;
it has the form "(U)" where U is a valid bracket sequence;
it has the form "VW" where V and W are valid bracket sequences.
For example, the sequence "(())()" is a valid bracket expression, but "((())(()" is not.

You are given a sequence of brackets S and you are allowed to rotate some of them. Bracket rotation means picking a single bracket and changing it into its opposite form (i.e. an opening bracket can be changed into a closing bracket and vice versa). The goal is to find the longest slice (contiguous substring) of S that forms a valid bracket sequence using at most K bracket rotations.

Write a function:

def solution(S, K)
that, given a string S consisting of N brackets and an integer K, returns the length of the maximum slice of S that can be transformed into a valid bracket sequence by performing at most K bracket rotations.

For example, given S = ")()()(" and K = 3, you can rotate the first and last brackets to get "(()())", which is a valid bracket sequence, so the function should return 6 (notice that you need to perform only two rotations in this instance, though).

Given S = ")))(((" and K = 2, you can rotate the second and fifth brackets to get ")()()(", which has a substring "()()" that is a valid bracket sequence, so the function should return 4.

Given S = ")))(((" and K = 0, you can't rotate any brackets, and since there is no valid bracket sequence with a positive length in string S, the function should return 0.

Assume that:

string S contains only brackets: '(' or ')';
N is an integer within the range [1..30,000];
K is an integer within the range [0..N].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N) (not counting the storage required for input arguments).
"""

from collections import deque

from measure import measure


# Correct but slow
def get_errors(S, L):
    errors = []
    open = deque()
    open_count = 0
    for i in range(L):
        cur = S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)


def get_sum(errors, L):
    if not errors:
        return L
    stops = errors[:]
    max_s = 0
    prev_stop = None
    stop = None
    for stop in stops:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s


def rotate(cur):
    if cur == '(':
        return ')'
    else:
        return '('


def get_change_points(S, L, errors):
    result = errors[:]
    if 0 not in errors:
        for i in range(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for i in range(L - 1, errors[-1], -1):
            cur = S[i]
            if cur == '(':
                result.append(i)
                break
    return result


@measure
def solution1(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors(S, L)
    if not initial_errors:
        return L
    max_len = get_sum(initial_errors, L)
    if K == 0:
        return max_len

    change_points = get_change_points(S, L, initial_errors)
    initial_errors = set(initial_errors)
    for i in range(len(change_points)):
        new_S = S[:]
        points = K
        left = None
        right = None
        for j in range(i, len(change_points)):
            change_point = change_points[j]
            prev_change_point = change_points[j - 1] if j - 1 >= 0 else None
            if left is None:
                left = new_S[change_point]
            elif right is None:
                right = new_S[change_point]
            if left and right:
                if left == right:
                    if prev_change_point not in initial_errors:
                        new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    elif change_point not in initial_errors:
                        new_S[change_point] = rotate(new_S[change_point])
                    elif left == '(':
                        new_S[change_point] = rotate(new_S[change_point])
                    else:
                        new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    points -= 1
                elif points >= 2:
                    new_S[prev_change_point] = rotate(new_S[prev_change_point])
                    new_S[change_point] = rotate(new_S[change_point])
                    points -= 2
                else:
                    break
                left = None
                right = None
                if points == 0:
                    break

        errors = get_errors(new_S, L)
        current_len = get_sum(errors, L)
        max_len = max(current_len, max_len)

    return max_len


# ****************************************
def get_errors2(S, L):
    errors = []
    open = deque()
    open_count = 0
    for i in range(L):
        cur = S[i]
        if cur == '(':
            open_count += 1
            open.append(i)
        else:
            if open_count == 0:
                errors.append(i)
            else:
                open_count -= 1
                open.pop()
    return errors + list(open)


def get_sum2(errors, L):
    if not errors:
        return L
    max_s = 0
    prev_stop = None
    stop = None
    for stop in errors:
        if prev_stop is None:
            s = stop
        else:
            s = stop - prev_stop - 1
        max_s = max(s, max_s)
        prev_stop = stop
    if stop is not None and stop < L - 1:
        max_s = max(max_s, L - stop - 1)
    return max_s


def rotate2(cur):
    if cur == '(':
        return ')'
    else:
        return '('


def get_change_points2(S, L, errors):
    result = errors[:]
    if 0 not in errors:
        for i in range(errors[0]):
            cur = S[i]
            if cur == ')':
                result = [i] + result
                break
    if L - 1 not in errors:
        for i in range(L - 1, errors[-1], -1):
            cur = S[i]
            if cur == '(':
                result.append(i)
                break
    return result


@measure
def solution2(S, K):
    S = list(S)
    L = len(S)
    if L <= 1:
        return 0

    initial_errors = get_errors2(S, L)
    if not initial_errors:
        return L
    max_len = get_sum2(initial_errors, L)
    if K == 0:
        return max_len
    # additional_change_points = get_change_points2(S, L, initial_errors)
    change_points = get_change_points2(S, L, initial_errors)
    initial_errors = set(initial_errors)
    results = {}
    last_changed = None
    for i in range(len(change_points)):
        processed = False
        if i - 2 >= 0 and i - 2 in results:
            processed = True
            result = results[i - 2]
            try:
                new_error_left_index = change_points[i]
                new_error_right_index = change_points[i + 1]
            except:
                break
            try:
                new_error_left = S[new_error_left_index]
                new_error_right = S[new_error_right_index]
            except:
                break

            try:
                drop_error_left_index = change_points[result - 1]
                drop_error_right_index = change_points[result]
                drop_error_left = S[drop_error_left_index]
                drop_error_right = S[drop_error_right_index]
            except:
                break

            if drop_error_left != drop_error_right or new_error_left != new_error_right:
                processed = False
            elif new_error_left_index not in initial_errors or new_error_right not in initial_errors or drop_error_left_index not in initial_errors or drop_error_right_index not in initial_errors:
                processed = False
            else:
                end = change_points[i + 2] if i + 2 < len(change_points) else L
                current_len = end - drop_error_right_index - 1
                max_len = max(current_len, max_len)
                results[i] = new_error_right_index

                if end == L:
                    break

        if not processed:
            new_S = S[:]
            points = K
            left = None
            right = None
            for j in range(i, len(change_points)):
                change_point = change_points[j]
                prev_change_point = change_points[j - 1] if j - 1 >= 0 else None
                if left is None:
                    left = new_S[change_point]
                elif right is None:
                    right = new_S[change_point]
                if left and right:
                    if left == right:
                        if prev_change_point not in initial_errors:
                            new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        elif change_point not in initial_errors:
                            new_S[change_point] = rotate2(new_S[change_point])
                        elif left == '(':
                            new_S[change_point] = rotate2(new_S[change_point])
                        else:
                            new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        points -= 1
                    elif points >= 2:
                        new_S[prev_change_point] = rotate2(new_S[prev_change_point])
                        new_S[change_point] = rotate2(new_S[change_point])
                        points -= 2
                    else:
                        last_changed = j
                        break
                    left = None
                    right = None
                    if points == 0:
                        last_changed = j
                        break

            errors = get_errors2(new_S, L)
            current_len = get_sum2(errors, L)
            max_len = max(current_len, max_len)
            results[i] = last_changed

    return max_len


# ************************************


@measure
def solution3(S, K):
    def get_errors(S, L):
        errors = []
        open = deque()
        open_count = 0
        for i in range(L):
            cur = S[i]
            if cur == '(':
                open_count += 1
                open.append(i)
            else:
                if open_count == 0:
                    errors.append(i)
                else:
                    open_count -= 1
                    open.pop()
        return errors + list(open)

    def get_sum(errors, L):
        if not errors:
            return L
        max_s = 0
        prev_stop = None
        stop = None
        for stop in errors:
            if prev_stop is None:
                s = stop
            else:
                s = stop - prev_stop - 1
            max_s = max(s, max_s)
            prev_stop = stop
        if stop is not None and stop < L - 1:
            max_s = max(max_s, L - stop - 1)
        return max_s

    def get_special_error_index(S, errors):
        prev_error = None
        for i in range(len(errors)):
            error = errors[i]
            if prev_error is not None:
                real_prev_error = S[prev_error]
                real_error = S[error]
                if real_prev_error != real_error:
                    return i - 1
            prev_error = error
        return None

    def _solution3(S, K):
        S = list(S)
        L = len(S)
        if L <= 1:
            return 0

        initial_errors = get_errors(S, L)

        special_error_index = get_special_error_index(S, initial_errors)

        if not initial_errors:
            return L
        max_len = get_sum(initial_errors, L)
        if K == 0:
            return max_len
        errors = initial_errors
        errors_len = len(errors)
        for i in range(errors_len):
            if special_error_index is not None:
                left_len = special_error_index - i - 1
            else:
                left_len = None
            special_error_inside = False
            # Get last fixed error
            fixed_errors_count = None
            end_error_index0 = i + K * 2 - 1
            if end_error_index0 >= errors_len:
                end_error_index0 = errors_len - 1
                fixed_errors_count = end_error_index0 - i + 1
                if fixed_errors_count % 2 == 1:
                    # Если исправили нечетное количество ошибок, последняя ошибка вылетает.
                    end_error_index0 -= 1

            if special_error_index is not None and i <= special_error_index < end_error_index0 and special_error_index + 1 <= end_error_index0 and left_len and left_len % 2 == 1:
                special_error_inside = True

            if fixed_errors_count is not None:
                points_left = K - fixed_errors_count / 2
            else:
                points_left = 0

            if special_error_inside and points_left < 1:
                end_error_index0 -= 2

            if end_error_index0 <= i:
                continue

            # end_error_index = errors[end_error_index0]

            # Get next error
            try:
                next_error_index0 = end_error_index0 + 1
                next_error_index = errors[next_error_index0]
            except:
                next_error_index = None

            # Get start
            if i == 0:
                start = 0
            else:
                prev_error_index = errors[i - 1]
                start = prev_error_index + 1

            # get length
            if next_error_index is not None:
                end = next_error_index
            else:
                end = L

            s = end - start
            max_len = max(s, max_len)

        return max_len

    if K > 0:
        S1 = list(S)
        S2 = list(S)
        L = len(S)
        for i in range(L):
            cur = S[i]
            if cur == ')':
                S1[i] = '('
                break
        for i in range(L - 1, -1, -1):
            cur = S[i]
            if cur == '(':
                S2[i] = ')'
                break
        sol1 = _solution3(S1[1:], K - 1)
        sol2 = _solution3(S2[:-1], K - 1)
    else:
        sol1 = sol2 = 0
    sol = _solution3(S, K)
    return max(sol, sol1, sol2)


# **********************************************


# 84%
@measure
def solution5(S, K):
    def _solution5(S, K):
        L = len(S)

        def get_sum(errors, L):
            if not errors:
                return L
            max_s = 0
            prev_stop = None
            stop = None
            for stop in errors:
                if prev_stop is None:
                    s = stop
                else:
                    s = stop - prev_stop - 1
                max_s = max(s, max_s)
                prev_stop = stop
            if stop is not None and stop < L - 1:
                max_s = max(max_s, L - stop - 1)
            return max_s

        def get_errors(S):
            opened = deque()
            errors = []
            for i in range(L):
                cur = S[i]
                if cur == '(':
                    opened.append(i)
                else:
                    if opened:
                        opened.pop()
                    else:
                        errors.append(i)
            while opened:
                errors.append(opened.pop())
            return sorted(errors)

        errors = get_errors(S)
        max_len = get_sum(errors, len(S))
        if K == 0:
            return max_len
        global_break = False
        for i in range(len(errors)):
            if global_break:
                break
            error_index1 = None
            error_index2 = None
            start_error_index = i
            j = i
            flags_left = K
            while j < len(errors):
                cur_error_index = errors[j]
                if error_index1 is None:
                    error_index1 = cur_error_index
                    j += 1
                elif error_index2 is None:
                    if j == len(errors) - 1:
                        global_break = True
                    error_index2 = cur_error_index
                    end = errors[j + 1] if j + 1 < len(errors) else L
                    error1 = S[error_index1]
                    error2 = S[error_index2]
                    if error1 == error2:
                        current_minus = 1
                        flags_left -= current_minus
                    else:
                        current_minus = 2
                        flags_left -= current_minus

                    error_index1 = None
                    error_index2 = None

                    if start_error_index == 0:
                        current_error_index = errors[start_error_index]
                        if current_error_index == 0:
                            start = errors[start_error_index]
                        else:
                            start = 0
                    else:
                        start = errors[start_error_index - 1] + 1

                    if flags_left >= 0:
                        current_len = end - start
                        max_len = max(current_len, max_len)

                    if flags_left <= 0:

                        flags_left += current_minus
                        break
                    else:
                        j += 1

        return max_len

    if K > 0:
        L = len(S)
        S1 = list(S)
        S2 = list(S)
        for i in range(L):
            cur = S[i]
            if cur == ')':
                S1[i] = '('
                break
        for i in range(L - 1, -1, -1):
            cur = S2[i]
            if cur == '(':
                S2[i] = ')'
                break
        sol1 = _solution5(S1[1:], K - 1)
        sol2 = _solution5(S2[:-1], K - 1)
    else:
        sol1 = 0
        sol2 = 0
    sol = _solution5(S, K)
    return max((sol1, sol2, sol))


# 100%!!!!
@measure
def solution7(S, K):
    def _solution(S, K):
        L = len(S)

        def get_sum(errors, L):
            if not errors:
                return L
            max_s = 0
            prev_stop = None
            stop = None
            for stop in errors:
                if prev_stop is None:
                    s = stop
                else:
                    s = stop - prev_stop - 1
                max_s = max(s, max_s)
                prev_stop = stop
            if stop is not None and stop < L - 1:
                max_s = max(max_s, L - stop - 1)
            return max_s

        def get_errors(S):
            opened = deque()
            errors = []
            for i in range(L):
                cur = S[i]
                if cur == '(':
                    opened.append(i)
                else:
                    if opened:
                        opened.pop()
                    else:
                        errors.append(i)
            while opened:
                errors.append(opened.pop())
            return sorted(errors)

        errors = get_errors(S)
        max_len = get_sum(errors, L)
        if K == 0 or max_len == L or max_len == L - 1:
            return max_len
        for i in range(2):
            global_break = False
            j = i
            flags_left = K
            minuses = deque()
            error_index1 = None
            error_index2 = None
            errors_len = len(errors)
            while j < errors_len:
                cur_error_index = errors[j]
                if error_index1 is None:
                    error_index1 = cur_error_index
                    j += 1
                elif error_index2 is None:
                    if j == errors_len - 1:
                        global_break = True
                    error_index2 = cur_error_index
                    end = errors[j + 1] if j + 1 < errors_len else L
                    error1 = S[error_index1]
                    error2 = S[error_index2]
                    if error1 == error2:
                        current_minus = 1
                    else:
                        current_minus = 2

                    while minuses and flags_left < current_minus:
                        minus = minuses.popleft()
                        flags_left += minus
                        i += 2

                    if i > 0:
                        start = errors[i - 1] + 1 if error_index1 > 0 else 0
                    else:
                        start = 0

                    if flags_left >= current_minus:
                        current_len = end - start
                        max_len = max(current_len, max_len)
                        j += 1
                        minuses.append(current_minus)
                        flags_left -= current_minus
                    else:
                        i += 2
                        j = i

                    error_index1 = None
                    error_index2 = None

                    if global_break:
                        break
        return max_len

    if K > 0:
        L = len(S)
        S = list(S)
        S1 = list(S)
        S2 = list(S)
        for i in range(L):
            cur = S[i]
            if cur == ')':
                S1[i] = '('
                break
        for i in range(L - 1, -1, -1):
            cur = S2[i]
            if cur == '(':
                S2[i] = ')'
                break
        if S1 != S:
            sol1 = _solution(S1[1:], K - 1)
        else:
            sol1 = 0
        if S2 != S:
            sol2 = _solution(S2[:-1], K - 1)
        else:
            sol2 = 0
    else:
        sol1 = 0
        sol2 = 0

    sol = _solution(S, K)
    return max((sol1, sol2, sol))


import random

variants = ['(', ')']

for k in range(10000):
    l = random.choice(list(range(1, 38)))
    K = random.choice(list(range(0, 5)))

    S = ''
    for i in range(l):
        variant = random.choice(variants)
        S += variant
    S1 = S[:]
    S2 = S[:]
    S3 = S[:]
    S4 = S[:]
    # print(S)
    sol7 = solution7(S1, K)
    sol1 = solution1(S, K)
    sol2 = solution2(S, K)
    sol3 = solution3(S2, K)
    if sol3 != sol7:
        print('S=', S, 'K=', K, 'sol3=', sol3, 'sol7=', sol7)

print(measure.timers)
# OrderedDict([('solution1', 0.497241735458374), ('solution2', 0.4474754333496094), ('solution3', 0.32116031646728516), ('solution5', 0), ('solution7', 0.31372594833374023)])
