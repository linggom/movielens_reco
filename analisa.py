import pickle
import numpy as np
import math

m = pickle.load(open("model/common/m.pkl")) 
nR = pickle.load(open("model/75/nR.pkl")) 


errord = []
for u in range(len(m)):
	for i in range(len(m[0])):
		if m[u][i] != 0:
			errord.append(math.pow(m[u][i]- nR[u][i], 2))

errord = np.array(errord)
print "ITEMS : " + str(len(m))
print "USERS : " + str(len(m[1]))
print "MSE : " + str(math.sqrt(np.sum(errord)/len(errord)))

