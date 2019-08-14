from include.setup import *

def classifier(id_log):

	print('Classifying IDs...')

	if TIMING: start = time.time()

	id_class = dict()
	id_period = dict()
	id_mean = dict()
	id_stdev = dict()

	for i in sorted(id_log.keys()):
		
		# classify type of periodic
		id_class[i] = ''

		# get interarrival times
		period = []
		for p in range(1, len(id_log[i])):
			period.append(id_log[i][p] - id_log[i][p-1])

		log = id_log[i]
		mean = statistics.mean(period)
		stdev = statistics.stdev(period)

		id_period[i] = period
		id_mean[i] = mean
		id_stdev[i] = stdev

		if strong_periodic(log, period, mean, stdev): #1
			id_class[i] = 'strong periodic'
		elif discontinuous_periodic(log, period, mean, stdev): #2
			id_class[i] = 'discontinuous periodic'
		elif dual_periodic(log, period, mean, stdev): #3
			id_class[i] = 'dual periodic' # 03B
		elif weak_periodic(log, period, mean, stdev): #6
			id_class[i] = 'weak periodic'
		elif miss_repeat(log, period, mean, stdev): #5
			id_class[i] = 'miss + repeat'
		elif miss_skip(log, period, mean, stdev): #4
			id_class[i] = 'miss + skip'
		else:
			id_class[i] = 'unclassified'
			#print(i, mean*1000, min(period)*1000, max(period)*1000)

	if STATS:
		print('         Strong: {} matches'.format( 
			sum(id_class[i] == 'strong periodic' for i in id_log.keys())))
		print('  Discontinuous: {} matches'.format(
			sum(id_class[i] == 'discontinuous periodic' for i in id_log.keys())))
		print('           Dual: {} matches'.format(
			sum(id_class[i] == 'dual periodic' for i in id_log.keys())))
		print('           Weak: {} matches'.format(
			sum(id_class[i] == 'weak periodic' for i in id_log.keys())))
		print('  Miss + Repeat: {} matches'.format(
			sum(id_class[i] == 'miss + repeat' for i in id_log.keys())))
		print('    Miss + Skip: {} matches'.format(
			sum(id_class[i] == 'miss + skip' for i in id_log.keys())))
		print('   Unclassified: {} matches'.format(
			sum(id_class[i] == 'unclassified' for i in id_log.keys())))
	if TIMING: print('Classifier ran in {:6f} seconds.'.format(time.time()-start))

	return id_class, id_period, id_mean, id_stdev

def strong_periodic(log, period, mean, stdev):
	if stdev < STRONG_THRESHOLD * mean:
		return True
	return False

def discontinuous_periodic(log, period, mean, stdev):
	if max(period) > DISCONTINUOUS_THRESHOLD * mean:
		return True
	return False

def dual_periodic(log, period, mean, stdev):
	p1 = [period[p] for p in range(0, len(period), 2)]
	p2 = [period[p] for p in range(1, len(period), 2)]
	return False

def weak_periodic(log, period, mean, stdev):
	return False

def miss_repeat(log, period, mean, stdev):
	return False

def miss_skip(log, period, mean, stdev):
	return False
