"""Game-agnostic illustrative arithmetic; not a Riftbound rules engine."""
import math
def hit(N,K,n):
    if not (isinstance(N,int) and isinstance(K,int) and isinstance(n,int) and 0<=K<=N and 0<=n<=N): raise ValueError("invalid population")
    return 1-(math.comb(N-K,n)/math.comb(N,n) if n<=N-K else 0)
def ev(weights,values):
    if len(weights)!=len(values) or not weights or any(w<0 for w in weights) or not math.isclose(sum(weights),1): raise ValueError("invalid weights")
    return sum(w*v for w,v in zip(weights,values))
def compare(a,b):
    if len(a)!=len(b) or not a: raise ValueError("incompatible vectors")
    return "A" if all(x>=y for x,y in zip(a,b)) and any(x>y for x,y in zip(a,b)) else "B" if all(y>=x for x,y in zip(a,b)) and any(y>x for x,y in zip(a,b)) else "undetermined"
def reject(f):
    try: f()
    except ValueError: return True
    return False
if __name__=="__main__":
    tests=[
    ("zero copies",lambda:hit(30,0,4)==0),
    ("certain draw",lambda:hit(30,30,1)==1),
    ("zero draws",lambda:hit(30,4,0)==0),
    ("source independent formula",lambda:math.isclose(hit(50,10,3),1-(40/50)*(39/49)*(38/48))),
    ("marginal diminishing reach",lambda:hit(40,2,5)-hit(40,1,5)>hit(40,3,5)-hit(40,2,5)),
    ("invalid population",lambda:reject(lambda:hit(40,41,5))),
    ("conditional expected utility",lambda:math.isclose(ev([.6,.4],[.7,.2]),.5)),
    ("invalid weights",lambda:reject(lambda:ev([.6,.5],[.7,.2]))),
    ("dominance requires all states",lambda:compare([.6,.5],[.5,.4])=="A"),
    ("tradeoff not dominance",lambda:compare([.6,.3],[.5,.5])=="undetermined"),
    ("equal not dominance",lambda:compare([.5,.5],[.5,.5])=="undetermined"),
    ("mismatched vectors",lambda:reject(lambda:compare([.5],[.5,.5])))
    ]
    for name,f in tests:
        assert f(),name
        print("PASS",name)
