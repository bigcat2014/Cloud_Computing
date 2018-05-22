#!/usr/bin/python3
import sys
import socket
import select
import enum
import re

HOST = ''
SOCKET_LIST = []
X_LIST = []
O_LIST = []
RECV_BUFFER = 4096
PORT = 9009
BOARD_SIZE = 9

have_enough_players = False


class Turn(enum.Enum):
	X_TURN = 'X'
	O_TURN = 'O'


class BoardValue(enum.Enum):
	X = 'X'
	O = 'O'
	EMPTY = '-'


class Winner(enum.Enum):
	X = 'X'
	O = 'O'
	DRAW = 'Draw'


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
				return Winner(current_val.value)
		
		# - - - - -
		# - - - - -
		# - o O o -
		# - - - - -
		# - - - - -
		if 1 <= coordinates[0] < BOARD_SIZE - 1:
			if (board[coordinates[0] - 1][coordinates[1]] == current_val and
					board[coordinates[0] + 1][coordinates[1]] == current_val):
				return Winner(current_val.value)
		
		if 1 <= coordinates[0] < BOARD_SIZE - 1 and 1 <= coordinates[1] < BOARD_SIZE - 1:
			# - - - - -
			# - o - - -
			# - - O - -
			# - - - o -
			# - - - - -
			if (board[coordinates[0] - 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] + 1][coordinates[1] - 1] == current_val):
				return Winner(current_val.value)
			# - - - - -
			# - - - o -
			# - - O - -
			# - o - - -
			# - - - - -
			elif (board[coordinates[0] - 1][coordinates[1] - 1] == current_val and
				  board[coordinates[0] + 1][coordinates[1] + 1] == current_val):
				return Winner(current_val.value)
		
		# o - - - -
		# - o - - -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[0] >= 2 and 1 <= coordinates[1] < BOARD_SIZE:
			if (board[coordinates[0] - 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] - 2][coordinates[1] + 2] == current_val):
				return Winner(current_val.value)
		
		# - - - - -
		# - - o - -
		# - - O - -
		# - - o - -
		# - - - - -
		if 1 <= coordinates[1] < BOARD_SIZE - 1:
			if (board[coordinates[0]][coordinates[1] - 1] == current_val and
					board[coordinates[0]][coordinates[1] + 1] == current_val):
				return Winner(current_val.value)
		
		# - - o - -
		# - - o - -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[1] < BOARD_SIZE - 2:
			if (board[coordinates[0]][coordinates[1] + 1] == current_val and
					board[coordinates[0]][coordinates[1] + 2] == current_val):
				return Winner(current_val.value)
		
		# - - - - o
		# - - - o -
		# - - O - -
		# - - - - -
		# - - - - -
		if coordinates[0] < BOARD_SIZE - 2 and coordinates[1] < BOARD_SIZE - 2:
			if (board[coordinates[0] + 1][coordinates[1] + 1] == current_val and
					board[coordinates[0] + 2][coordinates[1] + 2] == current_val):
				return Winner(current_val.value)
		
		# - - - - -
		# - - - - -
		# - - O o o
		# - - - - -
		# - - - - -
		if coordinates[0] < BOARD_SIZE - 2:
			if (board[coordinates[0] + 1][coordinates[1]] == current_val and
					board[coordinates[0] + 2][coordinates[1]] == current_val):
				return Winner(current_val.value)
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - - - o -
		# - - - - o
		if coordinates[0] < BOARD_SIZE - 2 and coordinates[1] >= 2:
			if (board[coordinates[0] + 1][coordinates[1] - 1] == current_val and
					board[coordinates[0] + 2][coordinates[1] - 2] == current_val):
				return Winner(current_val.value)
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - - o - -
		# - - o - -
		if coordinates[1] >= 2:
			if (board[coordinates[0]][coordinates[1] - 1] == current_val and
					board[coordinates[0]][coordinates[1] - 2] == current_val):
				return Winner(current_val.value)
		
		# - - - - -
		# - - - - -
		# - - O - -
		# - o - - -
		# o - - - -
		if coordinates[0] >= 2 and coordinates[1] >= 2:
			if (board[coordinates[0] - 1][coordinates[1] - 1] == current_val and
					board[coordinates[0] - 2][coordinates[1] - 2] == current_val):
				return Winner(current_val.value)
		
		for column in board:
			for tile in column:
				if tile == BoardValue.EMPTY:
					break
			else:
				continue
			break
		else:
			return Winner.DRAW
	
	return None


def check_move(board, move):
	move_good = True
	coordinates = []
	if re.match(r'^\(\d+,\s?\d+\)$', move):
		coordinates = list(map(int, re.findall(r'\d+', move)))
		coordinates = [element - 1 for element in coordinates]
		
		if len(coordinates) != 2:
			return False, coordinates
		if board[coordinates[0]][coordinates[1]] != BoardValue.EMPTY:
			return False, coordinates
		
		for num in coordinates:
			if num < 0 or num >= BOARD_SIZE:
				move_good = False
	else:
		move_good = False
	
	return move_good, coordinates


def get_game_board(board):
	return_string = ''
	length = len(board)
	for i in range(length - 1, -1, -1):
		return_string += str(i + 1)
		for j in range(0, len(board[i])):
			return_string += '\t'
			return_string += board[j][i].value
		return_string += '\n'
	
	for i in range(len(board)):
		return_string += '\t'
		return_string += str(i + 1)
	return return_string


def chat_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	
	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	
	global have_enough_players
	turn = Turn.X_TURN
	board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
	print("Chat server started on port " + str(PORT))
	
	while 1:
		
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
		
		for sock in ready_to_read:
			# a new connection request received
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				if len(SOCKET_LIST) % 2 == 0:
					X_LIST.append(sockfd)
					print("Client (%s,%s) connected as X" % addr)
					broadcast(server_socket, sockfd, "[%s:%s] entered our game as X\n" % addr)
					sockfd.send(str.encode("Current Game board:\n" + get_game_board(board) + "\n"))
					if have_enough_players:
						if turn == Turn.O_TURN:
							sockfd.send(str.encode('Waiting for other players to move...\n'))
							broadcast(server_socket, sockfd, 'Enter the coordinates of your next move (x, y):\n>> ')
						else:
							sockfd.send(str.encode('Enter the coordinates of your next move (x, y):\n>> '))
							broadcast(server_socket, sockfd, 'Waiting for other players to move...\n')
					else:
						sockfd.send(str.encode('Waiting for players...\n'))
				else:
					have_enough_players = True
					O_LIST.append(sockfd)
					print("Client (%s,%s) connected as O" % addr)
					broadcast(server_socket, sockfd, "[%s:%s] entered our game as O\n" % addr)
					sockfd.send(str.encode("Current Game board:\n" + get_game_board(board) + "\n"))
					if turn == Turn.X_TURN:
						sockfd.send(str.encode('Waiting for other players to move...\n'))
						broadcast(server_socket, sockfd, 'Enter the coordinates of your next move (x, y):\n>> ')
					else:
						sockfd.send(str.encode('Enter the coordinates of your next move (x, y):\n>> '))
						broadcast(server_socket, sockfd, 'Waiting for other players to move...\n')
			
			# a message from a client, not a new connection
			else:
				# process data recieved from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER).decode('utf-8')
					
					if data:
						# there is something in the socket
						move_good, coordinates = check_move(board, data)
						if move_good:
							if sock in X_LIST and turn == Turn.X_TURN:
								turn = Turn.O_TURN
								board[coordinates[0]][coordinates[1]] = BoardValue.X
								board_string = get_game_board(board) + '\n'
								sock.send(str.encode(board_string))
								broadcast(server_socket, sock, "X's move:\n" + board_string)
								
								winner = get_winner(board, coordinates)
								if winner == Winner.DRAW:
									sock.send(str.encode("The game was a draw.\n"))
									broadcast(server_socket, sock, "The game was a draw.\n")
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
									sock.send(str.encode('Enter the coordinates of your next move (x, y):\n>> '))
								elif winner:
									sock.send(str.encode("%s's have won the game\n" % winner.value))
									broadcast(server_socket, sock, "%s's have won the game\n" % winner.value)
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
									sock.send(str.encode(get_game_board(board) + '\nEnter the coordinates of your next move (x, y):\n>> '))
									broadcast(server_socket, sock, get_game_board(board) + '\nWaiting for other players to move...\n')
								else:
									sock.send(str.encode('Waiting for other players to move...\n'))
									broadcast(server_socket, sock, 'Enter the coordinates of your next move (x, y):\n>> ')
							
							elif sock in O_LIST and turn == Turn.O_TURN:
								turn = Turn.X_TURN
								board[coordinates[0]][coordinates[1]] = BoardValue.O
								board_string = get_game_board(board) + '\n'
								sock.send(str.encode(board_string))
								broadcast(server_socket, sock, "O's move:\n" + board_string)
								
								winner = get_winner(board, coordinates)
								if winner == Winner.DRAW:
									sock.send(str.encode("The game was a draw.\n"))
									broadcast(server_socket, sock, "The game was a draw.")
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
									sock.send(str.encode('Waiting for other players to move...\n'))
								elif winner:
									sock.send(str.encode("%s's have won the game\n" % winner.value))
									broadcast(server_socket, sock, "%s's have won the game\n" % winner.value)
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
									sock.send(str.encode(get_game_board(board) + '\nWaiting for other players to move...\n'))
									broadcast(server_socket, sock, get_game_board(board) + '\nEnter the coordinates of your next move (x, y):\n>> ')
								else:
									sock.send(str.encode('Waiting for other players to move...\n'))
									broadcast(server_socket, sock, 'Enter the coordinates of your next move (x, y):\n>> ')
							
							else:
								sock.send(str.encode("It is not your turn.\n"))
						else:
							sock.send(str.encode("Invalid move. Try again.\n>> "))
					
					else:
						# remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
						if sock in X_LIST:
							X_LIST.remove(sock)
						if sock in O_LIST:
							O_LIST.remove(sock)
						
						# at this stage, no data means probably the connection has been broken
						broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
						
						if have_enough_players and (len(X_LIST) == 0 or len(O_LIST) == 0):
							print("Not enough players. Exiting.\n")
							broadcast(server_socket, sock, "Not enough players. Exiting.\n")
							sys.exit(0)
				
				# exception
				except Exception:
					broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
					continue


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
		# send the message only to peer
		if socket != server_socket and socket != sock:
			try:
				socket.send(str.encode(message))
			except Exception:
				# broken socket connection
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)
				if socket in X_LIST:
					X_LIST.remove(socket)
				if socket in O_LIST:
					O_LIST.remove(socket)
				
				if have_enough_players and (len(X_LIST) == 0 or len(O_LIST) == 0):
					print("Not enough players. Exiting.\n")
					broadcast(server_socket, sock, "Not enough players. Exiting.\n")
					sys.exit(0)


if __name__ == "__main__":
	sys.exit(chat_server())
