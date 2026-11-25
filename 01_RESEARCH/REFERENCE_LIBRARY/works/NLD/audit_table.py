"""Reproduce p.21 arithmetic audit of the supplied PDF."""
import fitz,re,json,sys
from probability import tail
with fitz.open(sys.argv[1]) as doc:
    values=[float(x) for x in re.findall(r'(\d+(?:\.\d+)?)%',doc[20].get_text())]
assert len(values)==314
rows=[]
for j,v in enumerate(values):
    if j<90: grid,K,n,r='lower',j//3+1,7,j%3+1
    else: grid,K,n,r='upper',(j-90)%16+1,(j-90)//16+7,1
    expected=100*tail(60,K,n,r)
    rows.append(dict(grid=grid,K=K,n=n,r=r,printed=v,recalculated=round(expected,6),difference_pp=round(v-expected,6)))
errors=[x for x in rows if abs(x['difference_pp'])>0.011]
print(json.dumps({'cells_checked':len(rows),'tolerance_pp':0.011,'discrepancies':errors,'all_cells':rows},indent=2))
