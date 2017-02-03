import socket
import select
import os
import sys
import time
from threading import Thread

clients_info=[]

#Accepts a client connection
def accept_connection(main_connection, per_time, initial_hash):
	global clients_info
	while True:
		client, address = main_connection.accept()
		client.settimeout(5)
		client.send(per_time.encode())
		client.recv(1024)
		client.send(initial_hash.encode())
		try:
			clients_info.append(client)
		except socket.error:
			continue


def combi_manager():
	return "aaa"



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

	per_time = input("Enter per_time number ")
	initial_hash = input("Enter initial hash ")

	accept_connec_th = Thread(target=accept_connection, args=(main_connection, per_time, initial_hash), daemon=True)
	accept_connec_th.start()


	#Main Loop
	print("before loop")
	while(1):
		try:
			readable, writeable, exceptional = select.select(clients_info,[] ,[] ,0)
			#print("inside loop")
			for readable_sock in readable:
				msg = readable_sock.recv(1024)
				print(msg.decode())
				if(msg.decode() == "FOUND"):
					readable_sock.send(b"ok")
					print("Data found\n")
					sys.exit(0)
				else:
					starting_str = combi_manager()
					readable_sock.send(starting_str.encode())
				readable.remove(readable_sock)
		except socket.error:
			clients_info.remove(readable_sock)







	###Cleaning
	main_connection.close()

if __name__ == "__main__":
	main()
























