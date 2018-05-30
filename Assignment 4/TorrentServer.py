#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 3
#

import sys
import getopt
import socket


SHORT_OPTS = 'd'
LONG_OPTS = ['debug']
# Debug mode flag
DEBUG = False


def parse_args(argv):
	global DEBUG
	try:
		opts, remaining_args = getopt.getopt(args=argv, shortopts=SHORT_OPTS, longopts=LONG_OPTS)
		for opt, _ in opts:
			if opt == '-d' or opt == '--debug':
				DEBUG = True
	except getopt.GetoptError:
		return False
	
	if DEBUG:
		print('DEBUG mode')
	return True


def main():
	pass


if __name__ == '__main__':
	if not parse_args(sys.argv[1:]):
		sys.exit(1)
	main()
