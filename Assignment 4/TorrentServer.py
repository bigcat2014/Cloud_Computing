#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 3
#

import sys
import getopt
import socket
import json


SHORT_OPTS = 'd h'
LONG_OPTS = ['debug', 'help']
# Debug mode flag
DEBUG = False

HOST = ''
PORT = 9009
BUFFER_SIZE = 2048
ADDR = (HOST, PORT)
SERVER = socket.socket()
SERVER.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
SERVER.bind(ADDR)
ACK_STR = 'OK'


def usage():
	print('Only runs on Linux systems')
	print('Usage: ./TorrentServer.py [OPTION]...')
	print('Starts the torrent server and connects peers to other peers.\n')
	print('  -d, --debug\t\tEnable debug mode')
	print('  -h, --help\t\tDisplay this help and exit')


def parse_args(argv):
	global DEBUG
	try:
		opts, remaining_args = getopt.getopt(args=argv, shortopts=SHORT_OPTS, longopts=LONG_OPTS)
		for opt, value in opts:
			if opt == '-d' or opt == '--debug':
				DEBUG = True
			elif opt == '-h' or opt == '--help':
				usage()
				sys.exit(0)

	except getopt.GetoptError:
		return False
	
	if DEBUG:
		print('DEBUG mode')
	return True


def main():
	server_peer_ports = {}
	peers = []

	SERVER.listen(10)
	print('Waiting for connections...')

	try:
		while True:
			connection_fd, address = SERVER.accept()
			peers.append(address)

			print('Got connection from (%s:%s)' % address)

			if len(peers) == 1:
				if DEBUG:
					print('Client (%s:%s) is the server_peer\n' % address)

				connection_fd.send(bytes('server_peer', 'utf8'))
				server_peer_port = json.loads(connection_fd.recv(BUFFER_SIZE).decode('utf8'))
				
				try:
					server_peer_ports[address[0]] = server_peer_port
				except ValueError:
					print('server_peer error')
					sys.exit(1)

			else:
				if DEBUG:
					print('Client (%s:%s) is a client_peer\n' % address)
				
				connection_fd.send(bytes('client_peer', 'utf8'))
				
				ack = connection_fd.recv(BUFFER_SIZE).decode('utf8')
				if ack != ACK_STR:
					print('client_peer error')
					sys.exit(1)
				
				connection_fd.send(bytes(json.dumps(server_peer_ports), 'utf8'))
				
				ack = connection_fd.recv(BUFFER_SIZE).decode('utf8')
				if ack != ACK_STR:
					print('client_peer error')
					sys.exit(1)
			
			connection_fd.close()
	except KeyboardInterrupt:
		SERVER.close()
		print('\n')
		sys.exit(0)


if __name__ == '__main__':
	if not parse_args(sys.argv[1:]):
		sys.exit(1)
	main()
