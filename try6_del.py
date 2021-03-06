def check(start, end):
    if start>end:
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

    odd_list = [ ind for ind in range(len(A)) if A[ind]%2==1 ]

    if len(odd_list)%2==0:
        return check(0, len(A)-1)


    odd_list = [-1] + odd_list + [len(A)]
    res_cand = []
    # the numbers at the either end of A are even
    count = odd_list[1]
    second_count = len(A)-1-odd_list[-2]
    first_count = odd_list[2]-odd_list[1]-1
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

def iterate(a):
    l = len(a)
    for j in range(l):
        for i in range(1, l + 1- j):
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

#A = [1,1,2,2,2]
#A = [2, 2, 7, 2]
#A = [0,1,2,3,4,5]
#A = [4,5,3,7,2]

#A = [2, 4, 6, 1, 8, 2]
"""
sol1 = solution1(A)
sol2 = solution2(A)
print(sol1, sol2)
"""
"""
for cur, left, i, j in iterate(A):
    print(cur, left, i, j)
"""
#print(sol1, sol2)
import random, math

import time

time1 = 0
time2 = 0

for x in range(100):
    l = []
    for y in range(15):
        cur = math.ceil(random.random()*2)
        l.append(cur)
    start = time.time()
    sol1 = solution1(l)
    end = time.time()
    time1 += end - start
    start = time.time()
    sol2 = solution2(l)
    end = time.time()
    time2 += end - start
    if sol1 != sol2:
        print('sol1=', sol1,'sol2=', sol2, l)
end = time.time()

print(time1, time2)