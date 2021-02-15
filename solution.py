#import socket module
from socket import *
import sys # In order to terminate the program

def webServer(port=13331):
	serverSocket = socket(AF_INET, SOCK_STREAM)

	#Prepare a sever socket
	serverSocket.bind(("", port))
	serverSocket.listen(5)

	while True:
		#Establish the connection
		print('Ready to serve...')
		connectionSocket, addr = serverSocket.accept()
		try:
			message = connectionSocket.recv(1024)
			filename = message.split()[1]
			f = open(filename[1:])
			outputdata = f.read()

			#Send one HTTP header line into socket
			# header = "HTTP/1.1 200 OK\r\n\r\n"
			protocol = 'HTTP/1.1'
			status = '200'
			text = 'OK'
			connectionSocket.send(f"{protocol} {status} {text}\r\n\r\n".encode())

			#Send the content of the requested file to the client
			for i in range(0, len(outputdata)):
				connectionSocket.send(outputdata[i].encode())

			connectionSocket.send("\r\n".encode())
			connectionSocket.close()
		except IOError:
			#Send response message for file not found (404)
			# header = "\nHTTP/1.1 404 Not Found\n\n"
			protocol = 'HTTP/1.1'
			status = '404'
			text = 'Not Found'
			connectionSocket.send(f"{protocol} {status} {text}\r\n\r\n".encode())

			#Close client socket
			connectionSocket.close()

	serverSocket.close()
	sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
	webServer(13331)
