"""Least-squares calibration from CSV columns head_m,current_ma (traceable wet points)."""
import csv, math, json, argparse

def fit(points,pressure_pa=60000,density=998.2,gravity=9.80665):
 if len(points)<3 or any(not math.isfinite(x) or not math.isfinite(y) or x<0 or not 3.6<=y<=21 for x,y in points):
  raise ValueError('need >=3 finite, valid wet calibration points')
 x=sum(a for a,b in points)/len(points); y=sum(b for a,b in points)/len(points)
 ss=sum((a-x)**2 for a,b in points)
 if ss<=0: raise ValueError('depths must differ')
 slope=sum((a-x)*(b-y) for a,b in points)/ss
 if slope<=0: raise ValueError('non-positive slope')
 zero=y-slope*x; span=slope*pressure_pa/(density*gravity)
 residuals=[(b-zero)/slope-a for a,b in points]
 return dict(zero_ma=zero,span_ma=span,max_residual_mm=max(abs(r) for r in residuals)*1000,
             residuals_mm=[r*1000 for r in residuals],physical_accuracy_verified=False)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('csv');args=parser.parse_args()
 with open(args.csv) as f:points=[(float(r['head_m']),float(r['current_ma'])) for r in csv.DictReader(f)]
 print(json.dumps(fit(points),indent=2))
