import socket
import select
import os
import sys
import time
from threading import Thread

clients_info=[]

#Accepts a client connection
def accept_connection(main_connection, per_time, initial_hash):
	#A thread that accepts clients and send them parameters "per_time" && "initial_hash"

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


def combi_manager(combi_list, client): #stopped here
	return "aaa"


def combi_partitioner(combi_list, string_length, per_time): 
	#Fills the list "combi_list" example : 
	#per_time = 2 , string_length = 3
	#combi_list = ["aaa", "aac", "aae", ...]

	combi_list = []
	string = ['a'] * string_length

	combi_list.append(string)

	while(1):

		i = 0
		while(i < per_time):
			error = next_string_rec(string, string_length -1)
			if (error == -1):
				return(-1)
			i += 1
		combi_list.append(string)
		print(string)


def next_string_rec(string, current_case): 
	#recursive function to calculate the next string 
	#example: "aaa" => "aab"
	error = 0

	if(ord(string[current_case]) >= 122):
		if(current_case == 0):
			return(-1)
		string[current_case] = chr(ord(string[current_case]) - 26)
		error = next_string_rec(string, current_case-1)
	
	string[current_case] = chr(ord(string[current_case]) + 1) 

	return (error)


def main():

	Hash_type = ""
	Hash = ""
	combi_list = []

	main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # To refuse the socket if it is in time_wait
	main_connection.bind(("0.0.0.0", 5000))
	main_connection.listen(10)


	###############################################################
	#															  #
	###############################################################

	per_time = input("Enter per_time number ")
	initial_hash = input("Enter initial hash ")
	string_length = 2

	combi_partitioner(combi_list, string_length, int(per_time))

	accept_connec_th = Thread(target=accept_connection, args=(main_connection, per_time, initial_hash), daemon=True)
	accept_connec_th.start()

	#Main Loop
	print("before loop")
	while(1):
		try:
			readable, writeable, exceptional = select.select(clients_info,[] ,[] ,0)
			#print("inside loop")
			#print("------------------------------")
			#for l in clients_info:
			#	print(l)
			#print("------------------------------")
			for readable_sock in readable:
				msg = readable_sock.recv(1024)
				#print(msg.decode())
				if(msg.decode() == "FOUND"):
					readable_sock.send(b"ok")
					print("Data found\n")
					sys.exit(0)
				else:
					starting_str = combi_manager(combi_list, readable_sock)
					readable_sock.send(starting_str.encode())
				readable.remove(readable_sock)
		except socket.error:
			#If an error happens remove the client
			print("gtfo")
			clients_info.remove(readable_sock)

	#Cleaning all sockets
	for sock in clients_info:
		sock.close()
	main_connection.close()

if __name__ == "__main__":
	main()
