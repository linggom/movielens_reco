import pickle
import numpy as np
import math
import sys

TRESHOLD = 3
if len(sys.argv) > 1:
	user = int(sys.argv[1])
else:
	user = 1

nR = pickle.load(open("model/75/nR.pkl")) 
m = pickle.load(open("model/common/m.pkl")) 
movies = pickle.load(open("model/common/movies.pkl")) 
di = pickle.load(open("model/common/di.pkl")) 
dm = pickle.load(open("model/common/dm.pkl")) 
idi = pickle.load(open("model/common/idi.pkl")) 
idm = pickle.load(open("model/common/idm.pkl")) 

u = []
it = []
rat = []
preds = []
print(idm[user])
rec = {}
for idx, i in enumerate(nR[idm[user]]):
	real = m[user][idx]
	pred = i
	if (real == 0 and pred != 0):
		rec[movies[di[idx]]] = pred
		
import operator
sorted_x = sorted(rec.items(), key=operator.itemgetter(1))
sorted_x.reverse()
for i in sorted_x[:10]:
	print i
