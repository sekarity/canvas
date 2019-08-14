from include.setup import *

def enumerator(matches):

	print('Enumerating...')
	print(matches)

	network = []
	for pair in matches:
		exist = False
	#	print(pair[0], pair[1])
		for ecu in network:
			if pair[0] in ecu:
				exist = True
				if pair[1] not in ecu:
					ecu.append(pair[1])
			if pair[1] in ecu:
				exist = True
				if pair[0] not in ecu:
					ecu.append(pair[0])
		if exist == False:
			new = [pair[0], pair[1]]
			network.append(new)
	
	for ecu in network:
		print(sorted(ecu))
