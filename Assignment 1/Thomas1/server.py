#!/usr/bin/python3

import sys, getopt
import socket


def main(argv):
    # Debug mode flag
    DEBUG = False

    # Parse options for debug mode
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
    # Bind to the port
    s.bind((host, port))

    # Wait for client connection.
    s.listen(5)

    while True:
        # Establish connection with client.
        c, addr = s.accept()

        print('Got connection from %s\n' % str(addr))

        cumulString = ''
        numChars = 0
        numWords = 0
        numLines = 0

        print('Waiting to receive file...')
        # Wait for characters until an EOF character is received
        rec = c.recv(1024)
        while rec:
            if DEBUG:
                print('Length received: %d' % len(rec))
            # Accumulates the entire file
            cumulString += rec.decode('utf-8')
            # Temporarily store the current characters
            rec = c.recv(1024)

        print('Done.\n')

        # If a string exists, count the characters and words
        if cumulString:
            wordList = cumulString.split(' ')
            lineList = cumulString.split('\n')
            numChars = len(cumulString)
            numWords = len(wordList)
            numLines = len(lineList)

        print('Sending Data...')
        # Send the response with the number of characters and words to the client
        sendData = str.encode('File was received.\nThere are %d characters in the file\nThere are %d words in the file\nThere are %d lines in the file' % (numChars, numWords, numLines))
        c.send(sendData)
        print('Done.\n')

        # Close the connection
        c.close()
    # Close the session
    s.close()

if __name__ == '__main__':
    # Don't pass the script name
    main(sys.argv[1:])
