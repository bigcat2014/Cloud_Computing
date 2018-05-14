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
			if (board[coordinates[0] - 1][coordinates[1] - 1] == current_val and
						board[coordinates[0] - 2][coordinates[1] - 2] == current_val):
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
			if (board[coordinates[0] + 1][coordinates[1] + 1] == current_val and
						board[coordinates[0] + 2][coordinates[1] + 2] == current_val):
				return Winner(current_val.value)

		for column in board:
			if BoardValue.EMPTY in column:
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
	for i in range(len(board)):
		return_string += str(length - i)
		for tile in board[i]:
			return_string += '\t'
			return_string += tile.value
		return_string += '\n'
	
	return return_string


def chat_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	
	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	
	turn = Turn.X_TURN
	board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
	print("Chat server started on port " + str(PORT))
	
	while 1:
		
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
		
		for sock in ready_to_read:
			# a new connection request recieved
			if sock == server_socket:
				sockfd, addr = server_socket.accept()
				SOCKET_LIST.append(sockfd)
				if len(SOCKET_LIST) % 2 == 0:
					X_LIST.append(sockfd)
					print("Client (%s,%s) connected as X" % addr)
					broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room as X\n" % addr)
				else:
					O_LIST.append(sockfd)
					print("Client (%s,%s) connected as O" % addr)
					broadcast(server_socket, sockfd, "[%s:%s] entered our chatting room as O\n" % addr)
			
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
								broadcast(server_socket, sock, get_game_board(board))
								
								winner = get_winner(board, coordinates)
								if winner == Winner.DRAW:
									broadcast(server_socket, sock, "The game was a draw.")
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
								elif winner:
									broadcast(server_socket, sock, "%s's have won the game\n" % winner.value)
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
								
							elif sock in O_LIST and turn == Turn.O_TURN:
								turn = Turn.X_TURN
								board[coordinates[0]][coordinates[1]] = BoardValue.O
								broadcast(server_socket, sock, get_game_board(board))
								
								winner = get_winner(board, coordinates)
								if winner == Winner.DRAW:
									broadcast(server_socket, sock, "The game was a draw.")
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
								elif winner:
									broadcast(server_socket, sock, "%s's have won the game\n" % winner.value)
									turn = Turn.X_TURN
									board = [[BoardValue.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
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
				
				# exception
				except:
					broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
					continue
					

# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
		# send the message only to peer
		if socket != server_socket and socket != sock:
			try:
				socket.send(str.encode(message))
			except:
				# broken socket connection
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)
				if socket in X_LIST:
					X_LIST.remove(socket)
				if socket in O_LIST:
					O_LIST.remove(socket)


if __name__ == "__main__":
	sys.exit(chat_server())
