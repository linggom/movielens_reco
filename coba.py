import pickle
import numpy as np
import math
import sys

TRESHOLD = 3
if len(sys.argv) > 1:
	user = int(sys.argv[1])
else:
	user = 1

nR = pickle.load(open("model/15/nR.pkl")) 
m = pickle.load(open("model/15/m.pkl")) 
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
for idx, i in enumerate(nR[idm[user]]):
	real = m[user][idx]
	pred = i
	if (real != 0 or i != 0):
		u.append(user)
		it.append(movies[di[idx]])
		rat.append(i)
		preds.append(real)


import pandas as pd

df = pd.DataFrame(data=zip(u, it, rat, preds))
df.to_csv("result/hasil_"+str(user) + ".csv", index=False, header=("UserId", "movie", "prediction", "real"))
