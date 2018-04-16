#! usr/bin/python3

import sys, getopt
import socket

def main(argv):
	# Debug mode flag
	DEBUG = False
	# End Of File 'constant'
	EOF = '~'

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
	host = socket.gethostname()
	# Reserve a port for your service.
	port = 12345
	# Connect to the server
	s.connect((host, port))

	# Open the file for reading
	f = open('test.txt', 'r')

	print('Sending File...')
	# Read the file
	contents = f.read(1024)
	while contents:
		if DEBUG:
			print('Length sent: %d' % len(contents))
		# Send the file to the server
		s.send(contents)
		contents = f.read(1024)

	# Close the file
	f.close()

	# Send the End Of File character
	s.send(EOF)
	print('Done.\n')

	# Receive the response from the server
	rec = s.recv(1024)
	if DEBUG:
		print('Receiving Data...')
		print('Length: %d' % len(rec))
	
	# Print the response
	print(rec)

	# Close the socket
	s.close()

if __name__ == '__main__':
	main(sys.argv[1:])
