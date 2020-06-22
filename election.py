from collections import Counter
votes = []
while True:
    try:
        votes.append(list(input().strip()[::-1]))
    except EOFError:
        break
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

    print('The {}-th vote: {}'.format(i+1, obtained))
    if m == 1:
        print('  The candidate \'{}\' is the Final Winner !!'.format(top[0]))
        break
    elif m >= M:
        print('  All the candidates survived.')
        print('  Final winner was not determined.')
        break
    else:
        print('  Candidates {} survived.'.format([ obtained[j][0] for j in range(m)]))
    
    for n in range(N):
        while len(votes[n]) > 0 and not votes[n][-1] in candidates:
            votes[n].pop()
