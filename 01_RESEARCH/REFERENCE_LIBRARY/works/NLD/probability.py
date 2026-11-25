"""Exact sampling without replacement; NOT a game engine."""
from math import comb,isclose
from itertools import combinations
def tail(N,K,n,r):
    if not all(type(x)==int for x in (N,K,n,r)) or not (0<=K<=N and 0<=n<=N and r>=0):
        raise ValueError('invalid population/sample/threshold')
    return sum(comb(K,k)*comb(N-K,n-k) for k in range(max(r,0,n-(N-K)),min(K,n)+1))/comb(N,n)
def test():
    count=0
    for N in range(1,10):
        for K in range(N+1):
            for n in range(N+1):
                draws=list(combinations(range(N),n))
                for r in range(n+2):
                    exact=sum(sum(x<K for x in c)>=r for c in draws)/len(draws)
                    assert isclose(tail(N,K,n,r),exact,abs_tol=1e-12)
                    count+=1
    return count
if __name__=='__main__':
    print('PASS exhaustive cases:',test())
