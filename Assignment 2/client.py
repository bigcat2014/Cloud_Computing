#!/usr/bin/python3

from xmlrpc.client import ServerProxy


def main():
	adder = input('Please enter the adder server address\n>> ')
	multiplier = input('Please enter the multiplier server address\n>> ')
	
	adder_server = ServerProxy('http://' + adder + ':8000/')
	multiplier_server = ServerProxy('http://' + multiplier + ':8001/')
	
	multiplier_server.set_adder_server('http://' + adder + ':8000/')
	
	lines = []
	with open('test.txt', 'r') as f:
		line_strings = f.readlines()
	
	for string in line_strings:
		lines.append(string.split())
	
	for line in lines:
		if line[0] == 'A':
			print('Sum: %s' % adder_server.network_add(line[1], line[2]))
		elif line[0] == 'M':
			print('Product: %s' % multiplier_server.network_multiply(line[1], line[2]))


if __name__ == '__main__':
	main()
