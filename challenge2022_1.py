"""
You are given a string S consisting of letters 'a' and 'b'. The task is to rearrange letters in S so that it
contains three consecutive letters 'a' and three consecutive letters 'b'. What is the minimum necessary number of swaps of neighbouring letters to achieve this?

Write a function:

def solution(S)

that, given a string S of length N, returns the number of swaps after which S would contain "aaa" and "bbb" as
substrings. If it's not possible to rearrange the letters in such a way, the function should return −1.

Examples:

1. Given S = "ababab", the function should return 3. The sequence of swaps could be as follows: ababab → abaabb → aababb → aaabbb.

2. Given S = "abbbbaa", the function should return 4. The sequence of four swaps is: abbbbaa → babbbaa → bbabbaa → bbbabaa → bbbbaaa.

3. Given S = "bbbababaaab", the function should return 0. S already contains both "aaa" and "bbb" as substrings.

4. Given S = "abbabb", the function should return −1. It is not possible to obtain the required result from S as there are only two letters 'a'.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
string S consists only of the characters "a" and/or "b".
"""

# Gold https://app.codility.com/cert/view/certSV94GQ-MDUX7RXWQ7M4SWEC/
from measure import measure


# 62%, silver
@measure
def solution0(S):
    from collections import Counter
    def fix(v, letter):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(v)
        if v[0] == letter and v[1] == letter:
            result = [letter] * 3 + (L - 3) * [letter1], L - 3
        elif v[-1] == letter and v[-2] == letter:
            result = (L - 3) * [letter1] + [letter] * 3, L - 3
        else:
            sub_list = v[1: -1]
            a_pos = sub_list.index(letter)
            sub_list.insert(a_pos, letter)
            sub_list.insert(a_pos, letter)
            result1 = sub_list, L - 3
            a_pos = v.index(letter, 2)
            left = a_pos - 1
            right = L - a_pos - 2
            result2 = [letter] * 3 + (L - 3) * [letter1], left + right * 2
            result3 = (L - 3) * [letter1] + [letter] * 3, right + left * 2
            return result1, result2, result3
        return result,

    def brief_check(S):
        counter = Counter(S)
        for k in ('a', 'b'):
            if counter.get(k, 0) < 3:
                return -1
        S_string = S if isinstance(S, str) else ''.join(S)
        if 'aaa' in S_string and 'bbb' in S_string:
            return 0
        return 1

    def check(S, letter, is_nested=False):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(S)
        brief_result = brief_check(S)
        if brief_result <= 0:
            return brief_result
        S = list(S)
        current_steps = float('inf')

        current_list = []
        current_count = 0
        append = []

        for i in range(L):
            cur = S[i]
            if cur == letter:
                current_count += 1

            current_changed = False
            if cur == letter:
                current_list.append(cur)
                current_changed = True
            else:
                append.append(cur)

            if current_count >= 3:
                while True:
                    dropped_cand = current_list[0]
                    if dropped_cand == letter:
                        current_count_cand = current_count - 1
                        if current_count_cand < 3:
                            break
                        else:
                            current_count = current_count_cand
                            current_list.pop(0)
                            current_changed = True
                    elif dropped_cand != letter:
                        current_list.pop(0)
                if current_changed:
                    for fixed, cost in fix(current_list, letter):
                        contra_result = None
                        if not is_nested:
                            current_len = len(fixed) + len(append)
                            start_index = i + 1 - current_len
                            full_fixed = S[:start_index] + fixed + S[start_index + current_len:]
                            contra_result = check(full_fixed, letter1, is_nested=True)
                        if contra_result is not None:
                            cost += contra_result
                        if cost <= current_steps:
                            current_steps = cost
                            if cost == 1:
                                return 1
            current_list.extend(append)
            append = []
        return current_steps

    return min(check(S, 'a'), check(S, 'b'))

# Silver
@measure
def solution1(S):
    fixed_letters = {
        'a': 'aaa' in S,
        'b': 'bbb' in S,
    }

    def fix(v, letter):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(v)
        if v[0] == letter and v[1] == letter:
            result = [letter] * 3 + (L - 3) * [letter1], L - 3
        elif v[-1] == letter and v[-2] == letter:
            result = (L - 3) * [letter1] + [letter] * 3, L - 3
        else:
            sub_list = v[1: -1]
            a_pos = sub_list.index(letter)
            sub_list.insert(a_pos, letter)
            sub_list.insert(a_pos, letter)
            result1 = sub_list, L - 3
            a_pos = v.index(letter, 2)
            left = a_pos - 1
            right = L - a_pos - 2
            result2 = [letter] * 3 + (L - 3) * [letter1], left + right * 2
            result3 = (L - 3) * [letter1] + [letter] * 3, right + left * 2
            return result1, result2, result3
        return result,

    def brief_check(S):
        S_string = S if isinstance(S, str) else ''.join(S)
        if 'aaa' in S_string and 'bbb' in S_string:
            return 0
        return 1

    def get_side(v, letter, side):
        result = []
        count = 0
        if side == 'left':
            fixed_v = reversed(v)
        else:
            fixed_v = v
        for e in fixed_v:
            if e == letter:
                count += 1
            result.append(e)
            if count >= 2:
                if side == 'left':
                    result = list(reversed(result))
                return result
        return v

    def check(S, letter, is_nested=False):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(S)
        brief_result = brief_check(S)
        if brief_result <= 0:
            return brief_result
        S = list(S)
        current_steps = float('inf')

        current_list = []
        current_count = 0
        append = []

        for i in range(L):
            cur = S[i]
            if cur == letter:
                current_count += 1

            current_changed = False
            if cur == letter:
                current_list.append(cur)
                current_changed = True
            else:
                append.append(cur)

            if current_count >= 3:
                while True:
                    dropped_cand = current_list[0]
                    if dropped_cand == letter:
                        current_count_cand = current_count - 1
                        if current_count_cand < 3:
                            break
                        else:
                            current_count = current_count_cand
                            current_list.pop(0)
                            current_changed = True
                    elif dropped_cand != letter:
                        current_list.pop(0)
                if current_changed:
                    for fixed, cost in fix(current_list, letter):
                        contra_result = None
                        if not is_nested:
                            current_len = len(fixed) + len(append)
                            contra_fixed = fixed_letters[letter1]
                            if contra_fixed:
                                contra_result = 0
                            else:
                                start_index = i + 1 - current_len
                                left_side = S[: start_index]
                                left_side = get_side(left_side, letter1, 'left')
                                right_side = S[start_index + current_len:]
                                right_side = get_side(right_side, letter1, 'right')
                                full_fixed = left_side + fixed + right_side
                                contra_result = check(full_fixed, letter1, is_nested=True)
                        if contra_result is not None:
                            cost += contra_result
                        if cost <= current_steps:
                            current_steps = cost
                            if cost == 1:
                                return 1
            current_list.extend(append)
            append = []
        return current_steps

    result = min(check(S, 'a'), check(S, 'b'))
    if result == float('inf'):
        result = -1
    return result

# Gold
@measure
def solution(S):
    fixed_letters = {
        'a': 'aaa' in S,
        'b': 'bbb' in S,
    }

    def fix(v, letter):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(v)
        if v[0] == letter and v[1] == letter:
            result = [letter] * 3 + (L - 3) * [letter1], L - 3
        elif v[-1] == letter and v[-2] == letter:
            result = (L - 3) * [letter1] + [letter] * 3, L - 3
        else:
            sub_list = v[1: -1]
            a_pos = sub_list.index(letter)
            sub_list.insert(a_pos, letter)
            sub_list.insert(a_pos, letter)
            result1 = sub_list, L - 3
            a_pos = v.index(letter, 2)
            left = a_pos - 1
            right = L - a_pos - 2
            result2 = [letter] * 3 + (L - 3) * [letter1], left + right * 2
            result3 = (L - 3) * [letter1] + [letter] * 3, right + left * 2
            return result1, result2, result3
        return result,

    def brief_check(S):
        S_string = S if isinstance(S, str) else ''.join(S)
        if 'aaa' in S_string and 'bbb' in S_string:
            return 0
        return 1

    def check(S, letter, is_nested=False):
        if letter == 'a':
            letter1 = 'b'
        else:
            letter1 = 'a'
        L = len(S)
        brief_result = brief_check(S)
        if brief_result <= 0:
            return brief_result
        S = list(S)
        current_steps = float('inf')

        current_list = []
        current_count = 0
        append = []

        for i in range(L):
            cur = S[i]
            if cur == letter:
                current_count += 1

            current_changed = False
            if cur == letter:
                current_list.append(cur)
                current_changed = True
            else:
                append.append(cur)

            if current_count >= 3:
                while True:
                    dropped_cand = current_list[0]
                    if dropped_cand == letter:
                        current_count_cand = current_count - 1
                        if current_count_cand < 3:
                            break
                        else:
                            current_count = current_count_cand
                            current_list.pop(0)
                            current_changed = True
                    elif dropped_cand != letter:
                        current_list.pop(0)
                if current_changed:
                    for fixed, cost in fix(current_list, letter):
                        contra_result = None
                        if not is_nested:
                            current_len = len(fixed) + len(append)
                            contra_fixed = fixed_letters[letter1]
                            if contra_fixed:
                                contra_result = 0
                            else:
                                start_index = i + 1 - current_len
                                left_side = S[max(0, start_index - 2): start_index]
                                right_side = S[start_index + current_len: start_index + current_len + 2]
                                full_fixed = left_side + fixed + right_side
                                contra_result = check(full_fixed, letter1, is_nested=True)
                        if contra_result is not None:
                            cost += contra_result
                        if cost <= current_steps:
                            current_steps = cost
                            if cost == 1:
                                return 1
            current_list.extend(append)
            append = []
        return current_steps

    result = min(check(S, 'a'), check(S, 'b'))
    if result == float('inf'):
        result = -1
    return result


import random

chars = ['a', 'b'] * 100000
for _ in range(10000):
    S = random.sample(chars, 15000)
    S = ''.join(S)
    #while 'aaa' in S or 'bbb' in S:
    #    S = S.replace('aaa', 'aa')
    #    S = S.replace('bbb', 'bb')
    sol1 = solution1(S)
    sol = solution(S)
    if sol != sol1:
        print(sol1, sol)

S = 'bbbababababaa'
# S = 'abbababaababbabb'
sol1 = solution1(S)
sol = solution(S)
print(sol1, sol)

print(measure.timers)
