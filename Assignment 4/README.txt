/*
 *   Logan Thomas
 *   Cloud Computing Lab
 *   Assignment 4
 */

Setup:
    Download the files, open a terminal, and cd to the directory the files are stored in.
    Must be run on linux box


Running:
    Program can be run normally through the IDE's debugger or from the command line with
		$python [filename].py [args] online_book
		
		or
		
		$chmod +x [filename].py
		$./[filename].py [args]
	
	Server Args:
	    Usage: ./TorrentServer.py [OPTION]...

        Starts the torrent server and connects peers to other peers.

        Options:
          -d, --debug       Enable debug mode
          -h, --help        Display help and exit

	Client Args:
        ./Client.py [OPTION]... ADDRESS... PORT... PATH...

        Take the 50 most used words from the book provided in PATH and share with peers.
        Connects to the torrent server provided by ADDRESS and PORT to find peers.

        Options:
          -d, --debug       Enable debug mode
          -h, --help        Display help and exit