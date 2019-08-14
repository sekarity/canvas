from include.setup import *

def extractor(dump_file):

	print('Extracting data...')

	if TIMING: start = time.time()

	id_log = dict()

	for line in dump_file:
		
		if FORMAT == 'candump':
			l = line.split(' ')
			i = l[2].split('#')[0]
			t = float(l[0][1:-1])

		if i in id_log:
			id_log[i].append(t)
		else:
			id_log[i] = [t]
	
	if STATS: print('{:d} unique IDs found.'.format(len(id_log.keys())))
	if TIMING: print('Extractor ran in {:6f} seconds.'.format(time.time()-start))

	return id_log
