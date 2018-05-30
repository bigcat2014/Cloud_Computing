#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 3
#

import sys
import getopt
import os
import socket

SHORT_OPTS = 'd'
LONG_OPTS = ['debug']
# Debug mode flag
DEBUG = False
# Path to the book
PATH = 'http://www.gutenberg.org/files/863/863-0.txt'


def parse_args(argv):
	global DEBUG, PATH
	try:
		opts, remaining_args = getopt.getopt(args=argv, shortopts=SHORT_OPTS, longopts=LONG_OPTS)
		for opt, _ in opts:
			if opt == '-d' or opt == '--debug':
				DEBUG = True
	except getopt.GetoptError:
		return False
	
	if remaining_args is not None and len(remaining_args) != 0:
		PATH = remaining_args[0]
		if DEBUG:
			print('remaining_args is not None\n')
		
	else:
		if DEBUG:
			print('remaining_args is None')
	
	if DEBUG:
		print('DEBUG mode')
		print('PATH: %s' % (remaining_args[0]))
	return True


def main():
	book = os.system('wget %s' % PATH)
	if DEBUG:
		print('Book: %s' % str(book))
	

if __name__ == '__main__':
	if not parse_args(sys.argv[1:]):
		sys.exit(1)
	main()
