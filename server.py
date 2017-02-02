import socket
import os
import sys
import time
from threading import Thread

clients_info=[]

#Accepts a client connection
def accept_connection(main_connection, per_time):
	global clients_info
	while True:
		client, address = main_connection.accept()
		client.settimeout(5)
		try:
			client.send(per_time.encode())
			client.send(b"bbe")
			client.send(b"aaa")
			clients_info.append([client, address])
		except socket.error:
			continue


def main():

	Hash_type = ""
	Hash = ""




	main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # To refuse the socket if it is in time_wait
	main_connection.bind(("0.0.0.0", 5000))
	main_connection.listen(10)


	###############################################################
	#															  #
	###############################################################

	per_time = input("Enter per_time number")

	accept_connec_th = Thread(target=accept_connection, args=(main_connection, per_time), daemon=True)
	accept_connec_th.start()


	#Main Loop
	while(1):
		""








	###Cleaning
	client.close()
	main_connection.close()

if __name__ == "__main__":
	main()
























