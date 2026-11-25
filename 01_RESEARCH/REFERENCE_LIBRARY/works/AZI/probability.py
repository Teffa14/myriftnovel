from fractions import Fraction
from math import comb
from itertools import permutations
def H(N,K,n):
    return 1-Fraction(comb(N-K,n),comb(N,n)) if n<=N-K else Fraction(1)
def bridge(N,G,C,n,m):
    return H(N,G,n)+(H(N,G+C,n)-H(N,G,n))*H(N-n,G,m)
if __name__=="__main__":
    checks=0
    for N in range(3,9):
        for G in range(1,N):
            for C in range(N-G+1):
                for n in range(1,N):
                    for m in range(min(2,N-n)+1):
                        if n+m>5: continue
                        deck=['g']*G+['c']*C+['x']*(N-G-C)
                        total=hits=0
                        for a in permutations(range(N),n+m):
                            seq=[deck[i] for i in a]
                            hits+=('g' in seq[:n] or ('c' in seq[:n] and 'g' in seq[n:]))
                            total+=1
                        assert bridge(N,G,C,n,m)==Fraction(hits,total)
                        checks+=1
    print(checks)
