# Implementation of example 5.3

import math
import random
from collections import namedtuple
from itertools import product
from operator import itemgetter


ITERATIONS = 1000000

ACTIONS = range(2)
HIT, STICK = ACTIONS

CARDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

qs = {}
q_totals = {}
q_visits = {}


def iteration():
    hand = random.randrange(12, 22)
    showing = random.choice(CARDS)
    usable_ace = random.choice([True, False])
    dealer_hand = None

    seq = []

    while 1:
        # choose action
        if seq:
            max_q = -math.inf
            a = None
            for action in ACTIONS:
                q = qs.get(((hand, showing, usable_ace), action), 0)
                if (q > max_q):
                    max_q = q
                    a = action
        else:
            a = random.choice(ACTIONS)

        seq.append(((hand, showing, usable_ace), a))

        if a == HIT:
            hand += random.choice(CARDS)
            if hand > 21:
                if usable_ace:
                    hand -= 10
                    usable_ace = False
                else:
                    break

        # a == STICK
        else:
            dealer_hole = random.choice(CARDS)
            dealer_hand = showing + dealer_hole

            dealer_usable_ace = False
            if showing == 1 or dealer_hole == 1:
                dealer_hand += 10
                dealer_usable_ace = True

            while 1:
                if dealer_hand > 21:
                    if dealer_usable_ace:
                        dealer_hand -= 10
                        dealer_usable_ace = False
                    else:
                        break

                if dealer_hand >= 17:
                    break

                dealer_hand += random.choice(CARDS)

            break

    reward = None
    if hand > 21:
        reward = -1.0
    elif dealer_hand > 21 or hand > dealer_hand:
        reward = 1.0
    elif dealer_hand == hand:
        reward = 0.0
    else:
        reward = -1.0

    for sa in reversed(seq):
        q_totals[sa] = q_totals.get(sa, 0) + reward
        q_visits[sa] = q_visits.get(sa, 0) + 1
        qs[sa] = q_totals[sa] / q_visits[sa]


for i in range(ITERATIONS):
    iteration()

for sa, value in sorted(qs.items(), key=itemgetter(1)):
    print(sa, value, q_visits[sa])
print()

print('maximum visits:', max(q_visits.values()))
print('minimum visits:', min(q_visits.values()))
print()

print('   A2345678910')
for hand in reversed(range(12, 22)):
    s = str(hand) + ' '
    for showing in range(1, 11):
        if qs[((hand, showing, False), HIT)] > qs[((hand, showing, False), STICK)]:
            s += 'H'
        else:
            s += '.'
    print(s)

print()
for hand in reversed(range(12, 22)):
    s = str(hand) + ' '
    for showing in range(1, 11):
        if qs[((hand, showing, True), HIT)] > qs[((hand, showing, True), STICK)]:
            s += 'H'
        else:
            s += '.'
    print(s)

