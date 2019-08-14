from include.setup import *
from include.extractor import *
from include.classifier import *
from include.tracker import *
from include.enumerator import *

def main():

	# retrieve existing data or save new data
	if os.path.isfile('pickle/dump.dat'):
		with open('pickle/dump.dat', 'rb') as fp:
			if pickle.load(fp) == sys.argv[1]:
				id_log = pickle.load(fp)
				id_class = pickle.load(fp)
				id_period = pickle.load(fp)
				id_mean = pickle.load(fp)
				id_stdev = pickle.load(fp)
				id_list = pickle.load(fp)
			else:
				id_log, id_class, id_period, id_mean, id_stdev, id_list = store()
	else:
		id_log, id_class, id_period, id_mean, id_stdev, id_list = store()

	matches = []

	# iterate through each pair
	total_pairs = total_tracked = 0
	for i1 in range(len(id_list)):
		for i2 in range(i1, len(id_list)):

			# only compare pairs that don't match
			id1 = id_list[i1]
			id2 = id_list[i2]
			if id1 != id2:

				log1 = id_log[id1]
				log2 = id_log[id2]
				period1 = id_period[id1]
				period2 = id_period[id2]
				mean1 = id_mean[id1]
				mean2 = id_mean[id2]
				stdev1 = id_stdev[id1]
				stdev2 = id_stdev[id2]

				if id_class[id1] == id_class[id2] == 'strong periodic':
					if tracker(id1, id2, log1, log2, period1, period2, \
						mean1, mean2, stdev1, stdev2):
						matches.append((id1, id2))
					total_tracked += 1

				total_pairs += 1
				
	print('Total Pairs: {}'.format(total_pairs))
	print('Total Tracked: {}'.format(total_tracked))

	enumerator(matches)

def store():

	id_log = extractor(open(sys.argv[1], 'r'))
	id_class, id_period, id_mean, id_stdev = classifier(id_log)
	id_list = sorted(id_log.keys())

	with open('pickle/dump.dat', 'wb') as fp:
		pickle.dump(sys.argv[1], fp)
		pickle.dump(id_log, fp)
		pickle.dump(id_class, fp)
		pickle.dump(id_period, fp)
		pickle.dump(id_mean, fp)
		pickle.dump(id_stdev, fp)
		pickle.dump(id_list, fp)
	return id_log, id_class, id_period, id_mean, id_stdev, id_list

main()
