from collections import Counter, defaultdict
from random import randrange
from copy import deepcopy
import sys

def election(votes, message=True, force_forward=False):
    votes = deepcopy(votes)
    N = len(votes)
    for i in range(N):
        obtained = Counter([v[-1] for v in votes if len(votes)]).most_common()
        M = len(obtained)
        top = obtained[0]
        accum = [0]
        for ob in obtained[::-1]:
            accum.append(accum[-1] + ob[1])
        accum = accum[::-1]
        accum.pop()
        candidates = {top[0]}
        for m in range(1,M):
            if accum[m] < obtained[m-1][1]:
                break
            else:
                candidates.add(obtained[m][0])
        else:
            m += 1

        if message:
            print('The {}-th vote: {}'.format(i+1, obtained))
        if m == 1:
            return top[0]
        elif m >= M:
            if force_forward:
                l = M-2
                while l >= 0 and obtained[l][1] == obtained[-1][1]:
                    l -= 1
                candidates |= {obtained[i][0] for i in range(l+1,M)}
                candidates.discard(obtained[randrange(l+1,M)][0])
            elif message:
                print('  All the candidates survived.')
                print('  Final winner was not determined.')
                return None
        elif message:
            print('  Candidates {} survived.'.format([ obtained[j][0] for j in range(m)]))
        
        for n in range(N):
            while len(votes[n]) > 0 and not votes[n][-1] in candidates:
                votes[n].pop()

if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        K = 1
    else:
        K = int(args[1])

    votes = []
    while True:
        try:
            votes.append(list(input().strip().upper()[::-1]))
        except EOFError:
            break

    if K == 1:
        winner = election(votes)
        if winner:
            print('  The candidate \'{}\' is the Final Winner !!'.format(winner))
    else:
        win_times = defaultdict(int)
        for _ in range(K):
            win_times[election(votes, message=False, force_forward=True)] += 1
        print('  The winner distribution is: {}'.format(dict(win_times)))
