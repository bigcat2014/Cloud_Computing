#!/usr/bin/python3
#
#  Logan Thomas
#  Cloud Computing Lab
#  Assignment 3
#

import sys
import socket
import select

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009


def chat_server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server_socket.bind((HOST, PORT))
	server_socket.listen(10)
	
	# add server socket object to the list of readable connections
	SOCKET_LIST.append(server_socket)
	
	print("Chat server started on port " + str(PORT))
	
	while 1:
		
		# get the list sockets which are ready to be read through select
		# 4th arg, time_out  = 0 : poll and never block
		ready_to_read, ready_to_write, in_error = select.select(SOCKET_LIST, [], [], 0)
		
		for sock in ready_to_read:
			# a new connection_fd request recieved
			if sock == server_socket:
				connection_fd, addr = server_socket.accept()
				SOCKET_LIST.append(connection_fd)
				print("\rClient (%s,%s) connected" % addr)
				
				connection_fd.send(bytes("You can now start chatting!\n>>", "utf-8"))
				broadcast(server_socket, connection_fd, "\r[%s:%s] entered our chatting room\n>> " % addr)
			
			# a message from a client, not a new connection_fd
			else:
				# process data recieved from client,
				try:
					# receiving data from the socket.
					data = sock.recv(RECV_BUFFER).decode('utf-8')
					if data:
						# there is something in the socket
						broadcast(server_socket, sock, "\r%s: %s>> " % (str(sock.getpeername()), data))
						sock.send(bytes(">> ", "utf-8"))
					else:
						# remove the socket that's broken
						if sock in SOCKET_LIST:
							SOCKET_LIST.remove(sock)
						
						# at this stage, no data means probably the connection_fd has been broken
						print("\rClient (%s, %s) disconnected" % addr)
						broadcast(server_socket, sock, "\r(%s, %s) has left\n>> " % addr)
				
				# exception
				except:
					print("\rClient (%s, %s) disconnected" % addr)
					broadcast(server_socket, sock, "\r(%s, %s) has left\n>> " % addr)
					continue
	
	server_socket.close()


# broadcast chat messages to all connected clients
def broadcast(server_socket, sock, message):
	for socket in SOCKET_LIST:
		# send the message only to peers
		if socket != server_socket and socket != sock:
			try:
				socket.send(bytes(message, "utf-8"))
			except:
				# broken socket connection_fd
				socket.close()
				# broken socket, remove it
				if socket in SOCKET_LIST:
					SOCKET_LIST.remove(socket)


if __name__ == "__main__":
	sys.exit(chat_server())
