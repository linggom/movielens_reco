import numpy as np
import numpy
import pandas as pd
import pickle

def load():

	df = pd.read_csv("movies.dat", delimiter="::", header=None)
	udf = pd.read_csv("users.dat", delimiter="::", header=None)
	dicti = {}
	idicti = {}
	prefmap = {}
	itms = df.iloc[:, 0]
	for idx in range(len(itms)):
		dicti[idx] = itms[idx]
		idicti[itms[idx]] = idx

	i = [0] * len(itms)
	m = []
	dictm = {}
	idictm = {}
	usrs = udf.iloc[:, 0]
	for idx in range(len(usrs)):
		m.append(i)
		dictm[idx] = usrs[idx]
		idictm[usrs[idx]] = idx

	m = np.array(m)
	return m, dicti, dictm, idicti, idictm

def matrix_factorization(R, P, Q, K, steps=75, alpha=0.005, beta=0.05):
    Q = Q.T
    import datetime

    for step in xrange(steps):
    	print(step)
    	t0 = datetime.datetime.now()
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    	print(str(datetime.datetime.now() - t0))
    return P, Q.T

def load_prefs(m, di, dm, idi, idm):
	df = pd.read_csv("ratings.dat", delimiter="::", header=None)
	pref = {}
	for row in df.values:
		l = pref.get(row[0], [])
		l.append((row[1], row[2]))
		pref[row[0]] = l


	mtest = {}
	for k in pref.keys():
		mu = idm[k]
		print(k)
		prefs_ = pref[k]
		l  = len(prefs_)
		ltest = mtest.get(k, [])
		for idx, pref2 in enumerate(prefs_):
			if idx < int(0.7 * l):
				m[idm[k]][idi[pref2[0]]] = pref2[1]
			else:
				ltest.append((pref2[0], pref2[1]))
		mtest[k] = ltest
	return m, mtest

data = []
label = []
def load_prefs2(m, di, dm, idi, idm):
	from sklearn.cross_validation import KFold
	df = pd.read_csv("ratings.dat", delimiter="::", header=None)
	pref = {}
	for row in df.values:
		data.append([idm[row[0]], idi[row[1]]])
		label.append(row[2])
		
 	return m, []

m, di, dm, idi, idm = load()
m, mtest = load_prefs2(m, di, dm, idi, idm)


R = m

N = len(R)	
M = len(R[0])
K = 10

P = np.random.rand(N,K)
Q = np.random.rand(M,K)


nP, nQ = matrix_factorization(R, P, Q, K)
nR = np.dot(nP, nQ.T)
pickle.dump(nR, open("40.pkl", "w"))

