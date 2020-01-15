# Just some random implementations from the chapter on dynamic programming

import random
from itertools import product

import numpy as np
from matplotlib import pyplot


GAMMA = 1
THETA = .001


def print_grid(vs):
    print(vs[:4])
    print(vs[4:8])
    print(vs[8:12])
    print(vs[12:])


def policy_eval(S, A, R, p, policy):
    vs = np.zeros(len(S))
    while 1:
        print_grid(vs)

        delta = 0.0

        for i, s in enumerate(S):
            new_v = 0.0
            for a in A:
                total = 0.0
                for s2, r in product(S, R):
                    total += p(s2, r, s, a) * (r + GAMMA*vs[s2])
                new_v += policy(a, s) * total

            delta = max(delta, abs(new_v - vs[i]))
            vs[i] = new_v

        if delta < THETA:
            return vs


def example_4_1():
    S = range(15)
    A = range(4)  # north, south, east, west
    R = [-1.0, 0.0]

    def p(s2, r, s, a):
        if s == 0:
            if s == 0 and s2 == 0 and r == 0.0:
                return 1.0
            return 0.0

        if r != -1.0:
            return 0.0

        if a == 0:
            if s in [1, 2, 3]:
                if s2 == s:
                    return 1.0
                return 0.0
            if s in [4]:
                if s2 == 0:
                    return 1.0
                return 0.0
            if s - 4 == s2:
                return 1.0
            return 0.0
        if a == 1:
            if s in [12, 13, 14]:
                if s2 == s:
                    return 1.0
                return 0.0
            if s in [11]:
                if s2 == 0:
                    return 1.0
                return 0.0
            if s + 4 == s2:
                return 1.0
            return 0.0
        if a == 2:
            if s in [3, 7, 11]:
                if s2 == s:
                    return 1.0
                return 0.0
            if s in [14]:
                if s2 == 0:
                    return 1.0
                return 0.0
            if s + 1 == s2:
                return 1.0
            return 0.0
        if a == 3:
            if s in [4, 8, 12]:
                if s2 == s:
                    return 1.0
                return 0.0
            if s in [1]:
                if s2 == 0:
                    return 1.0
                return 0.0
            if s - 1 == s2:
                return 1.0
            return 0.0

    def policy(a, s):
        return 1.0/len(A)

    policy_eval(S, A, R, p, policy)


def example_4_1_test(X, Y):
    moves = []
    for i in range(100000):
        x = X
        y = Y
        m = 0
        while (x, y) not in [(0, 0), (3, 3)]:
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            x += dx
            y += dy
            if x < 0:
                x = 0
            if x > 3:
                x = 3
            if y < 0:
                y = 0
            if y > 3:
                y = 3
            m += 1
        moves.append(m)
    print(np.mean(moves))


def value_iteration(S, A, R, p):
    vs = np.zeros(len(S))
    while 1:
        print(vs)
        delta = 0.0
        for s in S:
            v = -np.inf
            for a in A(s):
                total = 0.0
                for s2, r in product(S, R):
                    total += p(s2, r, s, a) * (r + vs[s2])
                v = max(total, v)
            delta = max(delta, abs(vs[s] - v))
            vs[s] = v
        if delta < THETA:
            return vs


def exercise_4_9(ph):
    S = np.arange(101)
    R = [0.0, 1.0]

    def p(s2, r, s, a):
        if s in [0, 100]:
            if s2 in [0, 100] and r == 0.0:
                return 1.0
            return 0.0

        if s2 == min(s + a, 100):
            if s + a >= 100:
                if r == 1.0:
                    return ph
                return 0.0
            if r == 0.0:
                return ph
            return 0.0
        if s2 == s - a and r == 0.0:
            return 1.0 - ph
        return 0.0

    def A(s):
        return range(s+1)

    vs = value_iteration(S, A, R, p)
    policy = np.zeros(len(vs))
    for s in S:
        max_a = 0
        max_v = -np.inf
        for a in A(s):
            total = 0.0
            for s2, r in product(S, R):
                total += p(s2, r, s, a) * (r + GAMMA*vs[s2])
            if total > max_v:
                max_a = a
                max_v = total
        policy[s] = max_a

    pyplot.scatter(range(len(policy)), policy)
    pyplot.show()
