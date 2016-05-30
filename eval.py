


def load(data):
	u = []
	it = []
	p = []
	for k in data.keys(): 
		
		prefs = data[k].split(" ")
		c = 0
		for i in range(len(prefs)/2):
			u.append(k)
			it.append(prefs[c])
			p.append(prefs[c+1])
			c+=2
	return u,it,p


def write(u,i,p):
	f = open("hasil.csv", "w")
	for idx in range(len(u)):
		f.write("%s,%s,%s\n" % (u[idx], i[idx], p[idx]))
	f.close()
