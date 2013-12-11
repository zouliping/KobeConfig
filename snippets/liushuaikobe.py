def outputLskobe():
	lskobe = open(r'lskobe.txt', 'r')
	for line in lskobe:
		print line,

if  __name__ == '__main__':
	outputLskobe()
