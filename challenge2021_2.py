"""
During an Animal Day event, N people (numbered from 0 to N−1) showed up. Each of them had either a dog or a cat. The organizers decided to give them a wonderful gift: a toy for each animal.

After the event, it turned out that some people who owned a dog had received a cat-toy, and some people who owned a cat received a dog-toy. People may exchange toys, but only if they know each other (otherwise they have no way to contact the other person). The pair of people can exchange toys multiple times.

Knowing who knows who, who owns which animal, and what kind of toy he or she received, can you determine whether it is possible for people to exchange toys in such a way that every dog ends up with a dog-toy and every cat gets a cat-toy?

Write a function:

def solution(P, T, A, B)

that returns True if it is possible to exchange toys in such a way that every animal receives an appropriate toy, or False otherwise. First two arrays describe the pets (array P) and toys (array T) that every person owns. The J-th person owns pet P[J] and toy T[J] (1 means dog or dog-toy and 2 means cat or cat-toy). The next two arrays, A and B, both of length M, describe the relationships between people. For each integer K from 0 to M−1, person A[K] knows person B[K].

Examples:

1. Given:

P = [1, 1, 2]
T = [2, 1, 1]
A = [0, 2]
B = [1, 1]
the function should return True. Person 0 can exchange toys with person 1 to obtain a dog-toy, and then person 1 can exchange toys with person 2.

2. Given:

P = [2, 2, 1, 1, 1]
T = [1, 1, 1, 2, 2]
A = [0, 1, 2, 3]
B = [1, 2, 0, 4]
the function should return False. There is no way for persons 3 and 4 to exchange toys with others.

3. Given:

P = [1, 1, 2, 2, 1, 1, 2, 2]
T = [1, 1, 1, 1, 2, 2, 2, 2]
A = [0, 2, 4, 6]
B = [1, 3, 5, 7]
the function should return False. There is no way for persons 2 and 3 and for persons 4 and 5 to exchange toys with others.

4. Given:

P = [2, 2, 2, 2, 1, 1, 1, 1]
T = [1, 1, 1, 1, 2, 2, 2, 2]
A = [0, 1, 2, 3, 4, 5, 6]
B = [1, 2, 3, 4, 5, 6, 7]
the function should return True.

Write an efficient algorithm for the following assumptions:

N is an integer within the range [1..100,000];
M is an integer within the range [0..200,000];
each element of array ('P', 'T') is an integer that can have one of the following values: 1, 2;
each element of arrays A, B is an integer within the range [0..N−1];
for each integer K from 0 to M−1, elements A[K] and B[K] are different;
there are no redundant elements in arrays A, B; more formally every unordered pair of persons a, b will appear as A[K], B[K] for at most one K.
"""

#https://app.codility.com/cert/view/cert67KFA9-SYK995Y8P4BSQNJK/
from measure import measure

@measure
def solution(P, T, A, B):
    from collections import defaultdict
    res = all([p == t for p, t in zip(P, T)])
    if res:
        return True

    contacts = defaultdict(set)
    for a, b in zip(A, B):
        contacts[a].add(b)
        contacts[a].add(a)
        contacts[b].add(a)
        contacts[b].add(b)
    for person in range(len(P)):
        if person not in contacts:
            contacts[person] = []

    def get_nested_contacts(p):
        result = {p}
        current_contacts = contacts.get(p, set())
        while current_contacts:
            sub_contacts = [contacts[c] for c in current_contacts]
            new_potential_contacts = {c for e in sub_contacts for c in e}
            new_potential_contacts.difference(result)
            new_contacts = new_potential_contacts.difference(result)

            result.update(new_contacts)
            current_contacts = new_contacts
        return result

    visited = set()
    groups = []
    for p in range(len(P)):
        if p not in visited:
            c = get_nested_contacts(p)
            groups.append(c)
            visited.update(c)

    for g in groups:
        errors1 = [i for i in g if P[i] != T[i] and T[i] == 1]
        errors2 = [i for i in g if P[i] != T[i] and T[i] == 2]
        if len(errors1) != len(errors2):
            return False
    return True


P = [1, 1, 2, 1, 2]
T = [2, 1, 1, 2, 1]
A = [0, 2, 3]
B = [1, 1, 4]

# P = [1, 1, 2, 2, 1, 1, 2, 2]
# T = [1, 1, 1, 1, 2, 2, 2, 2]
# A = [0, 2, 4, 6]
# B = [1, 3, 5, 7]


# P = [1]
# T = [2]
# A = []
# B = []


# P = [2, 2, 2, 2, 1, 1, 1, 1] * 200
# T = [1, 1, 1, 1, 2, 2, 2, 2] * 200
# A = list(range(len(P) - 2))
# B = list(range(1, len(P) - 1))


# P = [2, 2, 2, 2, 1, 1, 1, 1]
# T = [1, 1, 1, 1, 2, 2, 2, 2]
# A = [0, 1, 2, 3, 4, 5, 6]
# B = [1, 2, 3, 4, 5, 6, 7]


sol = solution2(P, T, A, B)
print(sol)
print(measure.timers)
