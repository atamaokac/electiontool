from collections import Counter, defaultdict
from random import randrange
from copy import deepcopy
import sys

def election(votes, message=True, force_forward=False):
    votes = deepcopy(votes)
    N = len(votes)
    for i in range(N):
        obtained = Counter([v[-1] for v in votes if len(v)]).most_common()
        M = len(obtained)
        top = obtained[0]
        if M == 1:
            return top[0]

        accum = [0]
        for ob in obtained[::-1]:
            accum.append(accum[-1] + ob[1])
        accum = accum[:0:-1]
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
            l = M-2
            while l >= 0 and obtained[l][1] == obtained[-1][1]:
                l -= 1
            candidates = {obtained[i][0] for i in range(l+1)}
            fighting = {obtained[i][0] for i in range(l+1,M)}
            losers = set()
            for f in fighting:
                tmp_votes = deepcopy(votes)
                tmp_candidates = candidates | {f}
                for n in range(N):
                    while len(tmp_votes[n]) > 0 and not tmp_votes[n][-1] in tmp_candidates:
                        tmp_votes[n].pop()
                tmp_result = election(tmp_votes, message=False)
                if tmp_result != f and not (isinstance(tmp_result,list) and f in dict(tmp_result)):
                    losers.add(f)
            candidates |= fighting
            candidates -= losers
            if not losers:
                if message:
                    print('  All the candidates survived.')
                if force_forward:
                    drop = obtained[randrange(l+1,M)][0]
                    candidates.discard(drop)
                    if message:
                        print('  Drop the candidate \'{}\'.'.format(drop))
                elif message:
                    print('  Final winner was not determined.')
                    return obtained
        elif message:
            print('  Candidates {} survived.'.format([ obtained[j][0] for j in range(m)]))
        
        for n in range(N):
            while len(votes[n]) > 0 and not votes[n][-1] in candidates:
                votes[n].pop()

if __name__ == '__main__':
    args = sys.argv
    if len(args) <= 1:
        K = 0
    else:
        K = int(args[1])

    votes = []
    while True:
        try:
            votes.append(list(input().strip().upper()[::-1]))
        except EOFError:
            break

    if K == 0:
        winner = election(votes)
        if isinstance(winner, list):
            print('  The candidates \'{}\' are still surviving.'.format(winner))
        else:
            print('  The candidate \'{}\' is the Final Winner !!'.format(winner))
    else:
        win_times = defaultdict(int)
        for _ in range(K):
            win_times[election(votes, message=False, force_forward=True)] += 1
        result = list(win_times.items())
        if len(result) == 1:
            winner = result[0][0]
            print('  The candidate \'{}\' is the Final Winner !!'.format(winner))        
        else:
            print('  Final winner was not determined.')
            print('  The winner distribution is: {}'.format(dict(win_times)))
