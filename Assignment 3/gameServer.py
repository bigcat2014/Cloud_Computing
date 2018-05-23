#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 3
#

import sys
import socket
import select
import re
import enum
from collections import defaultdict


class Team(enum.Enum):
	X = 'X'
	O = 'O'

	def next(self):
		return Team.O if self == Team.X else Team.X


class Winner(enum.Enum):
	X = Team.X.name
	O = Team.O.name
	DRAW = "Draw"


class BoardValue(enum.Enum):
	X = Team.X.name
	O = Team.O.name
	EMPTY = '-'


def exception_handler(sock):
	# remove the socket that's broken
	if sock in SOCKET_LIST:
		SOCKET_LIST.remove(sock)
	if sock in X_TEAM:
		X_TEAM.remove(sock)
	if sock in O_TEAM:
		O_TEAM.remove(sock)

	if have_enough_players and (len(X_TEAM) == 0 or len(O_TEAM) == 0):
		print("Not enough players. Exiting.\n")
		broadcast(SOCKET_LIST, server_socket, None, "\nNot enough players. Exiting.\n")
		sys.exit()


# broadcast chat messages to all connected clients
def broadcast(socket_list, server_socket, sock, message):
	for socket in socket_list:
		# send the message only to peers
		if socket != server_socket and socket != sock:
			try:
				socket.send(bytes(message, "utf-8"))
			except:
				# broken socket connection_fd
				socket.close()
				# broken socket, remove it
				if sock in SOCKET_LIST:
					SOCKET_LIST.remove(sock)
				if sock in X_TEAM:
					X_TEAM.remove(sock)
				if sock in O_TEAM:
					O_TEAM.remove(sock)


def reset_board():
	global turn
	global board
	turn = Team.X
	board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def addToTeam(connection, addr):
	global have_enough_players
	team = ''

	SOCKET_LIST.append(connection)
	if len(SOCKET_LIST) % 2 == 0:
		X_TEAM.append(connection)
		team = Team.X.name
	else:
		have_enough_players = True
		O_TEAM.append(connection)
		team = Team.O.name

	print("\rClient ({ip}, {port}) connected as {team}".format(ip=addr[0], port=addr[1], team=team))
	broadcast(SOCKET_LIST, server_socket, None, "\r[{ip}:{port}] entered our game as {team}\n".format(ip=addr[0], port=addr[1], team=team))
	connection.send(bytes('Current board:\n{board}\n'.format(board=get_game_board(board)), "utf-8"))

	if have_enough_players:
		sendNewPlayerMessage(connection)
	else:
		broadcast(SOCKET_LIST, server_socket, None, 'Waiting for players...\n')


def sendNewPlayerMessage(connection):
	if turn == Team.X:
		broadcast(O_TEAM, server_socket, None, WAIT_PROMPT)
		broadcast(X_TEAM, server_socket, None, PROMPT)
	else:
		broadcast(X_TEAM, server_socket, None, WAIT_PROMPT)
		broadcast(O_TEAM, server_socket, None, PROMPT)


def prompt_players():
	global turn
	if turn == Team.X:
		broadcast(X_TEAM, server_socket, None, PROMPT)
		broadcast(O_TEAM, server_socket, None, WAIT_PROMPT)
	else:
		broadcast(O_TEAM, server_socket, None, PROMPT)
		broadcast(X_TEAM, server_socket, None, WAIT_PROMPT)


def check_move(board, move):
	move_good = True
	coordinates = []
	if re.match(r'^\(\d+,\s?\d+\)$', move):
		coordinates = list(map(int, re.findall(r'\d+', move)))
		coordinates = [element - 1 for element in coordinates]
		
		for num in coordinates:
			if num < 0 or num >= BOARD_SIZE:
				return False, coordinates

		if len(coordinates) != 2:
			move_good = False
		if board[coordinates[0]][coordinates[1]] != BoardValue.EMPTY:
			move_good = False
		
	else:
		move_good = False
	
	return move_good, coordinates


def make_move(sock, board, coordinates):
	global turn
	if (sock not in X_TEAM and turn == Team.X) or (sock not in O_TEAM and turn == Team.O):
		sock.send(str.encode("It is not your turn.\n"))
		return
	
	board[coordinates[0]][coordinates[1]] = BoardValue[turn.name]
	board_string = get_game_board(board) + '\n'
	broadcast(SOCKET_LIST, server_socket, None, "\n{turn}'s move:\n{board}".format(turn=turn.name, board=board_string))
	turn = turn.next()


def get_game_board(board):
	return_string = ''
	for i in range(BOARD_SIZE - 1, -1, -1):
		return_string += str(i + 1)
		for j in range(0, len(board[i])):
			return_string += '\t'
			return_string += board[j][i].value
		return_string += '\n'
	
	for i in range(len(board)):
		return_string += '\t'
		return_string += str(i + 1)
	return return_string


def get_winner(board, coordinates):
	if len(coordinates) == 2:
		current_val = board[coordinates[0]][coordinates[1]]
		if current_val == BoardValue.EMPTY:
			return None
		
		# - - - - -
		# - - - - -
		# o o O - -
		# - - - - -
		# - - - - -
		if coordinates[0] >= 2:
			if (board[coordinates[0] - 1][coordinates[1]] == current_val and
					board[coordinates[0] - 2][coordinates[1]] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - - - -
		# - o O o -
		# - - - - -
		# - - - - -
		if 1 <= coordinates[0] < BOARD_SIZE - 1:
			if (board[coordinates[0] - 1][coordinates[1]] == current_val and
					board[coordinates[0] + 1][coordinates[1]] == current_val):
				return Winner[current_val.value]
		
		if 1 <= coordinates[0] < BOARD_SIZE - 1 and 1 <= coordinates[1] < BOARD_SIZE - 1:
			# - - - - -
			# - o - - -
			# - - O - -
			# - - - o -
			# - - - - -
			if (board[coordinates[0] - 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] + 1][coordinates[1] - 1] == current_val):
				return Winner[current_val.value]
			# - - - - -
			# - - - o -
			# - - O - -
			# - o - - -
			# - - - - -
			elif (board[coordinates[0] - 1][coordinates[1] - 1] == current_val and
				  board[coordinates[0] + 1][coordinates[1] + 1] == current_val):
				return Winner[current_val.value]
		
		# o - - - -
		# - o - - -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[0] >= 2 and 1 <= coordinates[1] < BOARD_SIZE - 2:
			if (board[coordinates[0] - 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] - 2][coordinates[1] + 2] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - o - -
		# - - O - -
		# - - o - -
		# - - - - -
		if 1 <= coordinates[1] < BOARD_SIZE - 1:
			if (board[coordinates[0]][coordinates[1] - 1] == current_val and
					board[coordinates[0]][coordinates[1] + 1] == current_val):
				return Winner[current_val.value]
		
		# - - o - -
		# - - o - -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[1] < BOARD_SIZE - 2:
			if (board[coordinates[0]][coordinates[1] + 1] == current_val and
					board[coordinates[0]][coordinates[1] + 2] == current_val):
				return Winner[current_val.value]
		
		# - - - - o
		# - - - o -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[0] < BOARD_SIZE - 2 and coordinates[1] < BOARD_SIZE - 2:
			if (board[coordinates[0] + 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] + 2][coordinates[1] + 2] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - - - -
		# - - O o o
		# - - - - -
		# - - - - -
		if coordinates[0] < BOARD_SIZE - 2:
			if (board[coordinates[0] + 1][coordinates[1]] == current_val and
					board[coordinates[0] + 2][coordinates[1]] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - - - o -
		# - - - - o
		if coordinates[0] < BOARD_SIZE - 2 and coordinates[1] >= 2:
			if (board[coordinates[0] + 1][coordinates[1] - 1] == current_val and
					board[coordinates[0] + 2][coordinates[1] - 2] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - - o - -
		# - - o - -
		if coordinates[1] >= 2:
			if (board[coordinates[0]][coordinates[1] - 1] == current_val and
					board[coordinates[0]][coordinates[1] - 2] == current_val):
				return Winner[current_val.value]
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - o - - -
		# o - - - -
		if coordinates[0] >= 2 and coordinates[1] >= 2:
			if (board[coordinates[0] - 1][coordinates[1] - 1] == current_val and
					board[coordinates[0] - 2][coordinates[1] - 2] == current_val):
				return Winner[current_val.value]
		
		for column in board:
			for tile in column:
				if tile == BoardValue.EMPTY:
					return None

	return Winner.DRAW


def send_game_over():
	if winner == Winner.DRAW:
		broadcast(SOCKET_LIST, server_socket, None, "The game was a draw.\n")
		
	elif winner:
		broadcast(SOCKET_LIST, server_socket, None, "{winner}'s have won the game\n\n".format(winner=winner.value))
		
	reset_board()
	broadcast(SOCKET_LIST, server_socket, None, 'Current board:\n{board}\n'.format(board=get_game_board(board)))


HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009

X_TEAM = []
O_TEAM = []

BOARD_SIZE = 3
have_enough_players = False
turn = Team.X
board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
PROMPT = 'Enter your move (x, y)\n>> '
WAIT_PROMPT = 'Waiting for other players to move...\n'


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(10)

# add server socket object to the list of readable connections
SOCKET_LIST.append(server_socket)

print("Tic Tac Toe server started on port {port}".format(port=PORT))

while 1:
	
	# get the list sockets which are ready to be read through select
	# 4th arg, time_out  = 0 : poll and never block
	ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
	
	for sock in ready_to_read:
		# a new connection_fd request recieved
		if sock == server_socket:
			connection_fd, addr = server_socket.accept()
			addToTeam(connection_fd, addr)
		
		# a message from a client, not a new connection_fd
		else:
			# process data recieved from client,
			try:
				# receiving data from the socket.
				data = sock.recv(RECV_BUFFER).decode('utf-8')
				if data:
					# there is something in the socket
					move_good, coordinates = check_move(board, data)
					if move_good:
						make_move(sock, board, coordinates)
						winner = get_winner(board, coordinates)
						if winner:
							send_game_over()

						prompt_players()

					else:
						sock.send(str.encode("Invalid move. Try again.\n{prompt}".format(prompt=PROMPT)))
				else:
					print("\rClient ({ip}, {port}) disconnected".format(ip=addr[0], port=addr[1]))
					broadcast(SOCKET_LIST, server_socket, sock, "\r({ip}, {port}) has left\n".format(ip=addr[0], port=addr[1]))

					exception_handler(sock)

					prompt_players()
			
			# exception
			except Exception:
				broadcast(SOCKET_LIST, server_socket, None, "\rSomething went wrong and ({ip}, {port}) has left\n".format(ip=addr[0], port=addr[1]))
				exception_handler(sock)
				continue

server_socket.close()
