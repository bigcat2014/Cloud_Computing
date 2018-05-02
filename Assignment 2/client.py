#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 2
#

import getopt
import sys
from xmlrpc.client import ServerProxy


def main(argv):
	# Debug mode flag
	DEBUG = False
	
	try:
		opts, _ = getopt.getopt(argv, "d")
		for opt, _ in opts:
			if opt == '-d':
				DEBUG = True
	except getopt.GetoptError:
		pass
	
	adder = input('Please enter the adder server address\n>> ')
	multiplier = input('Please enter the multiplier server address\n>> ')
	
	adder_address = 'http://' + adder + ':8000/'
	multiplier_address = 'http://' + multiplier + ':8001/'
	
	if DEBUG:
		print('Setting up servers...')
		
	adder_server = ServerProxy(adder_address)
	if DEBUG:
		print('Adder server done.')
		
	multiplier_server = ServerProxy(multiplier_address)
	if DEBUG:
		print('Multiplier server done.\n')
	
	if DEBUG:
		print('Setting adder server on multiplier server')
	multiplier_server.set_adder_server(adder_address)
	
	if DEBUG:
		print('Adder server set on multiplier server\n')
	
	lines = []
	with open('test.txt', 'r') as f:
		line_strings = f.readlines()
	
	for string in line_strings:
		lines.append(string.split())
	
	for line in lines:
		if DEBUG:
			print('Line: %s' % line)
			
		if line[0] == 'A':
			print('Sum: %s' % adder_server.network_add(line[1], line[2]))
		elif line[0] == 'M':
			print('Product: %s' % multiplier_server.network_multiply(line[1], line[2]))
			
		if DEBUG:
			print('\n')


if __name__ == '__main__':
	main(sys.argv[1:])
