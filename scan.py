#!/usr/bin/python

import sys, getopt

def printSyntax():
	print('usage: python3 scan.py -s <subreddit_name> -t <text>')

def main(argv):
	subreddit = ''
	text = ''
	if len(sys.argv) != 5:
		print('Invalid number of arguments! Expected arguments: 5. Actual arguments: ', len(sys.argv))
		printSyntax()
		sys.exit()
	try:
		opts, args = getopt.getopt(argv,"s:t:",["subreddit=","text="])
	except getopt.GetoptError:
		printSyntax()
		print('b')
		sys.exit(2)
	
	for opt, arg in opts:
		if opt != '-s' and opt != '-t':
			printSyntax()
			print('c')
			sys.exit()
		elif opt in ("-s", "--subreddit"):
			subreddit = arg
		elif opt in ("-t", "--text"):
			text = arg
	print('Subreddit is: ', subreddit)
	print('Text is: ', text)

if __name__ == "__main__":
	main(sys.argv[1:])
