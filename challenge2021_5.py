"""
https://app.codility.com/programmers/task/partial_sort/
A string S is given. In one move, any two adjacent letters can be swapped. For example, given a string "abcd", it's possible to create "bacd", "acbd" or "abdc" in one such move. What is the lexicographically minimum string that can be achieved by at most K moves?

Write a function:

def solution(S, K)

that, given a string S of length N and an integer K, returns the lexicographically minimum string that can be achieved by at most K swaps of any adjacent letters.

Examples:

1. Given S = "decade" and K = 4, your function should return "adcede". Swaps could be:

decade → dceade,

dceade → dcaede,

dcaede → dacede,

dacede → adcede.

2. Given S = "bbbabbb" and K = 2, your function should return "babbbbb". The swaps are:

bbbabbb → bbabbbb,

bbabbbb → babbbbb.

3. Given S = "abracadabra" and K = 15, your function should return "aaaaabrcdbr".

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
string S consists only of lowercase letters ('a'-'z');
K is an integer within the range [0..1,000,000,000].
Not solved
"""

from string import ascii_lowercase
def solution0(S, K):
    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    for position in range(len(C)):
        if k_left <= 0:
            break
        current_list = C[position:position + k_left + 1]
        current_i = 0
        current_min = current_list[current_i]
        for i, e in enumerate(current_list):
            if k_left - i < 0:
                break
            if e < current_min:
                current_min = e
                current_i = i
        if current_i:
            k_left -= current_i
            next_elem = C.pop(position + current_i)
            C.insert(position, next_elem)

    return ''.join(key_map_rev[c] for c in C)




from string import ascii_lowercase
import bisect
from collections import defaultdict

def solutionNOTW(S, K):
    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    elems_positions = defaultdict(list)


    start = 0
    end = min(k_left, len(S))
    current_elems = C[:end]
    for i, e in enumerate(current_elems):
        elems_positions[e].append(i)

    sorted_elems = sorted(set(current_elems))
    while k_left and start < len(S):
        """
        I need to ensure that first elem is smallest
        """
        first_elem = current_elems[0]
        first_elem_pos = elems_positions[first_elem][0]
        res = []
        for e in sorted_elems:
            min_elem = e
            """
            I need to check if I can reach it
            """
            min_elem_pos = elems_positions[min_elem][0]
            distance = min_elem_pos - first_elem_pos
            if min_elem >= first_elem:
                res.append(first_elem)
                start += 1
                end += 1
            if distance <= k_left:
                pos = elems_positions[min_elem].pop(0)
                elems_positions[first_elem].pop(0)
                elems_positions[min_elem].insert(0, first_elem_pos)
                #elems_positions[first_elem].insert(0, first_elem_pos + 1)
                if not elems_positions[first_elem]:
                    ind = bisect.bisect_left(sorted_elems, first_elem)
                    sorted_elems.pop(ind)
                res.append(min_elem)
                k_left -= distance
                start += 1
                end += 1
                current_elems.pop(pos)

                break
    return res





from string import ascii_lowercase
import bisect
from collections import defaultdict
# 84%
def solutionFEFE(S, K):
    def simple_solution(C, K):
        k_left = K
        for position in range(len(C)):
            if k_left <= 0:
                break
            current_list = C[position:position + k_left + 1]
            current_i = 0
            current_min = current_list[current_i]
            for i, e in enumerate(current_list):
                if k_left - i < 0:
                    break
                if e < current_min:
                    current_min = e
                    current_i = i
            if current_i:
                k_left -= current_i
                next_elem = C.pop(position + current_i)
                C.insert(position, next_elem)

        return C

    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    result = []
    for elem in sorted(set(C)):
        positions = []
        for i, e in enumerate(C):
            if e == elem:
                positions.append(i)
        for i, position in enumerate(positions):
            if position - i > k_left:
                result += simple_solution(C, k_left)
                return ''.join(key_map_rev[c] for c in result)
            k_left -= (position - i)
            if k_left >= 0:
                result.append(elem)
                C.pop(position - i)
            else:
                k_left += (position - i)

    return ''.join(key_map_rev[c] for c in result + C)





from string import ascii_lowercase
import bisect
from collections import defaultdict
# 84%
def solutionEWSEF(S, K):
    def simple_solution(C, K):
        return C

    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    result = []
    for elem in sorted(set(C)):
        positions = []
        for i, e in enumerate(C):
            if e == elem:
                positions.append(i)
        for i, position in enumerate(positions):
            if position - i > k_left:
                result += simple_solution(C, k_left)
                return ''.join(key_map_rev[c] for c in result)
            k_left -= (position - i)
            if k_left >= 0:
                result.append(elem)
                C.pop(position - i)
            else:
                k_left += (position - i)

    return ''.join(key_map_rev[c] for c in result + C)





from string import ascii_lowercase
from collections import defaultdict

def solutionFDDF(S, K):
    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    result = []
    while k_left and C:
        min_e = C[0]
        min_i = 0
        for i in range(k_left + 1):
            try:
                e = C[i]
            except IndexError:
                break
            if e < min_e or e == 0:
                min_e = e
                min_i = i
                if e == 0:
                    break
        result.append(C.pop(min_i))
        k_left -= min_i
    return ''.join(key_map_rev[c] for c in result + C)


from string import ascii_lowercase
from collections import defaultdict
import bisect

def solution(S, K):
    key_map = {s: i for (i, s) in enumerate(ascii_lowercase)}
    key_map_rev = {i: s for (i, s) in enumerate(ascii_lowercase)}
    C = [key_map[s] for s in S]
    k_left = K
    result = []
    counts = defaultdict(int)

    c = C[:k_left]
    sorted_c = sorted(c)
    for e in c:
        counts[e] += 1

    while k_left:
        min_elem = sorted_c[0]
        min_elem_pos = next(e for e in C[:k_left] if e == min_elem)
        try:
            C.pop(min_elem_pos)
        except IndexError:
            break

        counts[min_elem] -= 1
        result.append(min_elem)
        if not counts[min_elem]:
            del counts[min_elem]
            sorted_c.pop(0)
        k_left -= min_elem_pos
        if not min_elem_pos:
            try:
                new_elem = C[k_left]
            except IndexError:
                pass
            else:
                counts[new_elem] += 1
                bisect.insort_left(sorted_c, new_elem)

    return ''.join(key_map_rev[c] for c in result + C)


S = 'abfdhfhfgracadabdrewra'
#S = 'bbaa'
K = 6

sol0 = solution0(S, K)
sol = solution(S, K)
print(sol, sol0, sol0==sol)
