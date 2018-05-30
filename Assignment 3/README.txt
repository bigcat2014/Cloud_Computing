/*
 *   Logan Thomas
 *   Cloud Computing Lab
 *   Assignment 3
 */

Setup:
    Download the files, open a terminal, and cd to the directory the files are stored in


Running:
    Program can be run normally through the IDE's debugger or from the command line with
		$python [filename].py [args]
		
		or
		
		$chmod +x [filename].py
		$./[filename].py [args]
	
	For messaging system:
		On one linux box, start chatServer.py
		Take note of the public ip address of this machine and the port the server was started on.
		
		On another linux box, start client.py and give it the public ip and the port of the chat
		server.
		
		$./client.py [ip] [port]
		
		Now you should be able to chat with other clients!
		Note: You can start up to 10 clients
	
	For Tic Tac Toe:
		On one linux box, start gameServer.py
		Take note of the public ip address of this machine and the port the server was started on.
		
		On another linux box, start client.py and give it the public ip and the port of the game
		server.
		
		$./client.py [ip] [port]
		
		Now you should be able to play tic tac toe with other clients!
		Note: You can start up to 10 clients