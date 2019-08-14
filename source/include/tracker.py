from include.setup import *

def tracker(id1, id2, log1, log2, a1, a2, p1, p2, s1, s2):

	l = lcm(round(p1*1000), round(p2*1000))/1000
	n = l/p1
	m = l/p2	

	d = []
	cycle = 0
	while cycle < math.floor(min(len(log1)/round(n), len(log2)/round(m))):
		t1 = log1[cycle*round(n)]
		t2 = log2[cycle*round(m)]
		t1mt2 = t1-t2	
		d.append(t1mt2)
		cycle = cycle + 1
	
	if len(d) > 10:
		delta = statistics.stdev(d)
		if delta < 0.001000:
			#print('{} {} {:17.6f} {:17.6f} {:17.6f}'.format( \
			#	id1, id2, p1, p2, statistics.stdev(d))) 
			return True
	
	return False

def lcm(x, y):
	return abs(x * y) / fractions.gcd(x, y) if x and y else 0

def search(log, target):

	i = bisect.bisect_left(log, target)

	if i == 0:
		return log[0]
	if i == len(log):
		return log[-1]

	left = log[i-1]
	right = log[i]

	if right - target < target - left:
		return right
	else:
		return left
