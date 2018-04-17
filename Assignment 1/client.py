#!/usr/bin/python3

import sys, getopt
import socket

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

	# Create a socket object
	s = socket.socket()
	# Get public ip address
	host = input("Enter the hostname\n>> ")
	# Reserve a port for your service.
	port = 12345
	# Connect to the server
	s.connect((host, port))

	print('Sending File...')

	# Open the file for reading
	with open('test.txt', 'r') as f:
		# Read the file
		contents = f.read(1024)
		while contents:
			if DEBUG:
				print('Length sent: %d' % len(contents))
			# Send the file to the server
			s.send(str.encode(contents))
			contents = f.read(1024)

	print('Done.\n')
	s.shutdown(socket.SHUT_WR)

	# Receive the response from the server
	rec = s.recv(1024)
	if DEBUG:
		print('Receiving Data...')
		print('Length: %d' % len(rec))
	
	# Print the response
	print(rec.decode('utf-8'))

	# Close the socket
	s.close()

if __name__ == '__main__':
	main(sys.argv[1:])
