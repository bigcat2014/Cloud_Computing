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
import pathlib
import json
from operator import itemgetter 
import string

SHORT_OPTS = 'd h'
LONG_OPTS = ['debug', 'help']
# Debug mode flag
DEBUG = False
# Path to the book
# http://www.gutenberg.org/files/863/863-0.txt
PATH = ''
SERVER_ADDR = ''
SERVER_PORT = 0
SERVER = socket.socket()
SERVER_PEER_SOCK = socket.socket()
SERVER_PEER_ADDR = ''
SERVER_PEER_PORT = 9000
BUFFER_SIZE = 4096
ACK_STR = 'OK'


def usage():
	print('Only runs on Linux systems')
	print('Usage: ./Client.py [OPTION]... ADDRESS... PORT... PATH...')
	print('Take the 50 most used words from the book provided in PATH and share with peers.')
	print('Connects to the torrent server provided by ADDRESS and PORT to find peers.\n')
	print('  -d, --debug\t\tEnable debug mode')
	print('  -h, --help\t\tDisplay this help and exit')


def parse_args(argv):
	global DEBUG, PATH, SERVER_ADDR, SERVER_PORT
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

	try:
		SERVER_ADDR = remaining_args[0]
		SERVER_PORT = int(remaining_args[1])
		PATH = remaining_args[2]

	except (IndexError, ValueError):
		return False	
	
	if DEBUG:
		print('DEBUG mode')
		print('PATH: %s' % (PATH))
		print('Server at: (%s:%s)' % (SERVER_ADDR, SERVER_PORT))

	return True


def count_words(book):
	wordDict = {}
	bookList = book.read().split()
	exclude = set(string.punctuation)
	for word in bookList:
		word = ''.join(ch for ch in word if ch not in exclude)
		if len(word) >= 5:
			if word in wordDict.keys():
				wordDict[word] += 1
			else:
				wordDict[word] = 1
	return sorted(wordDict.items(), key=itemgetter(1))[-50:]


def handle_word_list(word_list, recv_word_list):
	recv_words_dict = dict(recv_word_list)
	common_word_list = []
	for word, value in word_list:
		if word in recv_words_dict.keys():
			common_word_list.append((word, value + recv_words_dict[word]))

	print('Common words:')
	for word, count in common_word_list:
		print('\t%s: %s' % (word, count))


def main():
	split_path = PATH.split('/')
	tail = split_path[len(split_path) - 1]
	file_path = pathlib.Path(tail)
	book = None

	if file_path.is_file():
		if DEBUG:
			print('Book already exists')
	else:
		if DEBUG:
			print('Book does not exist\nDownloading...')
		os.system('wget %s' % PATH)
	if file_path.is_file():
		book = file_path.open()
	else:
		print('File not found: %s' % file_path)
		sys.exit(1)

	if DEBUG:
		print('Book: ')
		os.system('head -n2 %s' % tail)

	# Count words
	word_list = count_words(book)

	SERVER.connect((SERVER_ADDR, SERVER_PORT))
	ack = SERVER.recv(BUFFER_SIZE).decode('utf8')
	if ack == 'server_peer':
		if DEBUG:
			print('I am the server_peer')

		SERVER_PEER_SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		SERVER_PEER_SOCK.bind((SERVER_PEER_ADDR, SERVER_PEER_PORT))
		SERVER_PEER_SOCK.listen(10)
		SERVER.send(bytes(json.dumps(SERVER_PEER_PORT), 'utf8'))
		print('Server peer started at (%s:%s)' % (SERVER_PEER_ADDR, SERVER_PEER_PORT))

		try:
			while True:
				client_peer, address = SERVER_PEER_SOCK.accept()
				print('\nGot connection from (%s:%s)' % address)

				client_peer.send(bytes(json.dumps(word_list), 'utf8'))

				recvWordList = json.loads(client_peer.recv(BUFFER_SIZE).decode('utf8'))

				if DEBUG:
					print('word_list[:5]: %s\n' % str(word_list[:5]))
					print('recvWordList[:5]: %s\n' % str(recvWordList[:5]))
				
				client_peer.send(bytes(ACK_STR, 'utf8'))

				handle_word_list(word_list, recvWordList)

				client_peer.close()

		except KeyboardInterrupt:
			SERVER_PEER_SOCK.close()
			print('\n')
			sys.exit(0)

	elif ack == 'client_peer':
		if DEBUG:
			print('I am the clientPeer')
		SERVER.send(bytes(ACK_STR, 'utf8'))

		peers = json.loads(SERVER.recv(BUFFER_SIZE).decode('utf8'))
		SERVER.send(bytes(ACK_STR, 'utf8'))

		for addr in peers:
			if DEBUG:
				print('Connecting to server_peer (%s:%s)' % (addr, peers[addr]))
			server_peer = socket.socket()
			server_peer.connect((addr, peers[addr]))
			print('Connected to peer server at (%s:%s)' % (addr, peers[addr]))

			recvWordList = json.loads(server_peer.recv(BUFFER_SIZE).decode('utf8'))

			server_peer.send(bytes(json.dumps(word_list), 'utf8'))

			if DEBUG:
				print('word_list[:5]: %s\n' % str(word_list[:5]))
				print('recvWordList[:5]: %s\n' % str(recvWordList[:5]))			
			
			server_peer.recv(BUFFER_SIZE)

			handle_word_list(word_list, recvWordList)

	else:
		print('Server error')
		sys.exit(1)


if __name__ == '__main__':
	if not sys.platform.startswith('linux'):
		usage()
		sys.exit(1)
	if not parse_args(sys.argv[1:]):
		usage()
		sys.exit(1)
	main()
