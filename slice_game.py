# -*- coding: utf-8 -*-
"""
https://codility.com/programmers/custom_challenge/scandium2016/
Even sums is a game for two players. Players are given a sequence of N positive integers and take turns alternately. In each turn, a player chooses a non-empty slice (a subsequence of consecutive elements) such that the sum of values in this slice is even, then removes the slice and concatenates the remaining parts of the sequence. The first player who is unable to make a legal move loses the game.

You play this game against your opponent and you want to know if you can win, assuming both you and your opponent play optimally. You move first.

Write a function:

def solution(A)

that, given a zero-indexed array A consisting of N integers, returns a string of format "X,Y" where X and Y are, respectively, the first and last positions (inclusive) of the slice that you should remove on your first move in order to win, assuming you have a winning strategy. If there is more than one such winning slice, the function should return the one with the smallest value of X. If there is more than one slice with the smallest value of X, the function should return the shortest. If you do not have a winning strategy, the function should return "NO SOLUTION".

For example, given the following array:

  A[0] = 4
  A[1] = 5
  A[2] = 3
  A[3] = 7
  A[4] = 2
the function should return "1,2". After removing a slice from positions 1 to 2 (with an even sum of 5 + 3 = 8), the remaining array is [4, 7, 2]. Then the opponent will be able to remove the first element (of even sum 4) or the last element (of even sum 2). Afterwards you can make a move that leaves the array containing just [7], so your opponent will not have a legal move and will lose. One of possible games is shown on the following picture:



Note that removing slice "2,3" (with an even sum of 3 + 7 = 10) is also a winning move, but slice "1,2" has a smaller value of X.

For the following array:

  A[0] = 2
  A[1] = 5
  A[2] = 4
the function should return "NO SOLUTION", since there is no strategy that guarantees you a win.

Assume that:

N is an integer within the range [1..100,000];
each element of array A is an integer within the range [1..1,000,000,000].
Complexity:

expected worst-case time complexity is O(N);
expected worst-case space complexity is O(N), beyond input storage (not counting the storage required for input arguments).
Elements of input arrays can be modified.

Первое решение - не мое.
"""

def check(start, end):
    if start > end:
        res = 'NO SOLUTION'
    else:
        res = str(start) + ',' + str(end)

    return res

def trans( strr ):
    if strr =='NO SOLUTION':
        return (-1, -1)
    else:
        a, b = strr.split(',')
        return ( int(a), int(b) )


def solution1(A):
    # write your code in Python 2.7

    odd_list = [ind for ind in range(len(A)) if A[ind] % 2 ==1]
    # Получаем список нечетных индексов

    if len(odd_list) % 2 == 0:
        # Если четное количество нечетных, то это сразу победа.
        # Логично. Ведь если сумма - четная, то мы не можем разбить на четное и нечетное. То есть хода короче не будет.
        return check(0, len(A)-1)
        # Фрматирует вывод

    odd_list = [-1] + odd_list + [len(A)]
    # Прибавляем к нечетным индектам слева -1 и справа - длину исходного массива(несуществующий индекс)
    res_cand = []
    # the numbers at the either end of A are even
    count = odd_list[1]
    # Берем изначально первый нечетный индекс
    second_count = len(A)-1-odd_list[-2]
    # Вычитаем из последнего индеса последний четный индекс(-2 потому, что мы туда прибавляли)
    first_count = odd_list[2]-odd_list[1]-1
    # Вычитаем из второго нечетного индекса первый и еще 1
    if second_count >= count:
        res_cand.append(  trans(check( odd_list[1]+1, len(A)-1-count )))

    if first_count >= count:
        res_cand.append(  trans(check( odd_list[1]+count+1, len(A)-1 )))

    twosum = first_count + second_count
    if second_count < count <= twosum:
        res_cand.append(  trans(check( odd_list[1]+(first_count-(count-second_count))+1, odd_list[-2] )))

    ###########################################
    count = len(A)-1-odd_list[-2]
    first_count = odd_list[1]
    second_count = odd_list[-2]-odd_list[-3]-1
    if first_count >= count:
        res_cand.append(  trans(check( count, odd_list[-2]-1 )))

    if second_count >= count:
        res_cand.append(  trans(check( 0, odd_list[-2]-count-1)) )

    twosum = first_count + second_count
    if second_count < count <= twosum:
        res_cand.append(  trans(check( count-second_count, odd_list[-3])) )



    res_cand = sorted( res_cand, key=lambda x: (-x[0],-x[1]) )

    cur = (-1, -2)
    for item in res_cand:
        if item[0]!=-1:
            cur = item

    return check( cur[0], cur[1] )

#***********************************************
# My extremely slow
def iterate(a):
    l = len(a)
    for j in range(l): # Первый символ
        for i in range(1, l + 1- j): # Длина
            cur = a[j:j + i]
            if sum(cur) % 2 == 1:
                continue
            left = a[:j] + a[j + i:]
            yield (cur, left, i, j)


def initial_move(a):
    l = len(a)
    if l == 1:
        if a[0] % 2 == 0:
            return (0, 0)
        else:
            return None

    for cur, left, i, j in iterate(a):
        res = check_left2(left)
        if res:
            return (j, j + i - 1)

def check_left1(a):
    # Здесь ход делает первый игрок. То есть нужно, чтобы была хоть одна правильная
    # То есть крутимся, пока не получим True от второго.
    # Или если выигрыш в 1 ход, например четный остсток
    # Есди поражение в 1 ход, товетка неправильноя, False
    l = len(a)
    if l == 1:
        if a[0] % 2 == 0:
            return True
        else:
            return False
    if sum(a) % 2 == 0:
        return True

    for cur, left, i, j in iterate(a):
        res = check_left2(left)
        if res:
            return True
    return False

def check_left2(a):
    # Это ход игрока 2. Тут нам нужно, чтобы ни один из его ходов не давал победы.
    # То есть крутимся, пока не получим False
    # Если здесь победа в 1 ход - вернем False, тк ни одной правильной ветки отсюда нет
    # Если поражение в 1 ход - вернем True
    l = len(a)
    if not a:
        return True

    if l == 1:
        if a[0] % 2 == 0:
            return False
        else:
            return True
    if sum(a) % 2 == 0:
        return False

    for cur, left, i, j in iterate(a):
        res = check_left1(left)
        if not res:
            return False
    return True

def solution2(a):
    res = initial_move(a)
    if res:
        return "{},{}".format(res[0], res[1])
    else:
        return "NO SOLUTION"

#***********************************************
"""
Тут мы исходим из того, что для победы в остатке должно быть только одно нечетное число посередние, а слева и справа поровну четных
"""
# My some errors + slow
def solution3(a):
    L = len(a)
    def iterate_array(a):
        for j in range(L):  # Первый символ
            for i in range(1, L + 1 - j):  # Длина
                cur = a[j:j + i]
                if sum(cur) % 2 == 1:
                    continue
                left = a[:j] + a[j + i:]
                if left and sum(left) % 2 == 0:
                    continue
                yield (left, i, j)

    def _solution(a):
        for left, i, j in iterate_array(a):
            if not left:
                return (0, len(a) - 1)
            if L == 1:
                return (j, j + i - 1)
            elif L == 2:
                continue
            odd_count = 0
            left_even_count = 0
            right_even_count = 0
            odd_index = None
            for s in left:
                if s % 2 == 1:
                    odd_count += 1
                    odd_index = j
                else:
                    if odd_index is None:
                        left_even_count += 1
                    else:
                        right_even_count += 1
                if odd_count == 2:
                    break
            if odd_count == 1 and left_even_count == right_even_count:
                return j, j + i - 1

    res = _solution(a)
    if res:
        return "{},{}".format(res[0], res[1])
    else:
        return "NO SOLUTION"

# My 100%
def solution4(A):
    def _format_result(result):
        if result:
            return "{},{}".format(result[0], result[1])
        else:
            return "NO SOLUTION"

    def _solution(A, L, reversed):
        first_evens_count = 0
        odds_count = 0
        second_evens_count = 0
        odd_index = None
        for i in range(L):
            cur = A[i]
            if cur % 2 == 0:
                if odds_count == 0:
                    first_evens_count += 1
                elif odds_count == 1:
                    second_evens_count += 1
            else:
                odds_count += 1
                if odd_index is None:
                    odd_index = i

            if odds_count == 2 or second_evens_count == first_evens_count:
                required_evens_count = first_evens_count - second_evens_count
                first_index = odd_index + second_evens_count + 1
                if not reversed:
                    for j in range(L - 1, odd_index, -1):
                        if required_evens_count == first_evens_count:
                            break
                        cur = A[j]
                        if cur % 2 == 0:
                            required_evens_count += 1
                            second_evens_count -= 1
                            first_index -= 1


                second_index = L - required_evens_count
                slice_to_check = A[first_index: second_index]
                if slice_to_check and sum(slice_to_check) % 2 == 0:
                    left = A[second_index:]
                    if all(i % 2 == 0 for i in left):
                        return first_index, second_index - 1
                return

    L = len(A)
    if L == 1:
        if A[0] % 2 == 0:
            return _format_result((0, 0))
        else:
            return _format_result(None)
    result_candidates = []
    if sum(A) % 2 == 0:
        result_candidates.append((0, L - 1))
    if sum(A[:-1]) % 2 == 0 and A[-1] % 2 == 1:
        result_candidates.append((0, L - 2))
    if sum(A[1:]) % 2 == 0 and A[0] % 2 == 1:
        result_candidates.append((1, L - 1))

    B = list(reversed(A))
    result = _solution(B, L, reversed=True)
    if not result:
        result = _solution(A, L, reversed=False)
    else:
        result = (L - result[1] - 1, L - result[0] - 1)
    if result:
        result_candidates.append(result)

    if not result_candidates:
        return _format_result(None)
    best = result_candidates[0]
    iter_candidates = result_candidates.__iter__()
    iter_candidates.__next__()
    for candidate in iter_candidates:
        if candidate[0] <= best[0] and candidate[1] <= best[1]:
            best = candidate

    return _format_result(best)



A = [1]
sol4 = solution4(A)
sol1 = solution1(A)
print(sol1, sol4)

import os
os._exit(0)


#A = [2, 2, 7, 2]
#A = [1,2,3,4,5]
#A = [4,5,3,7,2]
#A = [1, 2, 3, 4]

#A = [2, 2, 2, 2, 1, 2, 2, 2, 1, 1, 2, 2]
#A = [2, 2, 3, 3, 3, 2, 2, 2]

sol1 = solution1(A)
sol2 = solution2(A)
sol4 = solution4(A)
print(sol1, sol2, sol4)

"""
for cur, left, i, j in iterate(A):
    print(cur, left, i, j)
"""
#print(sol1, sol2)
import random, math

import time
# print(sol1, sol2)
import math
import random
import time

time1 = 0
time2 = 0
time4 = 0

for x in range(100):
    l = []
    for y in range(229):
        cur = math.ceil(random.random()*2)
        l.append(cur)
    start = time.time()
    sol1 = solution1(l)
    end = time.time()
    time1 += end - start

    start = time.time()
    #sol2 = solution2(l)
    end = time.time()
    time2 += end - start

    start = time.time()
    sol4 = solution4(l)
    end = time.time()
    time4 += end - start
    #print(l, sol2)
    if sol1 != sol4:
        print('sol1=', sol1,'sol4=', sol4, l)


print(time1, time2, time4)