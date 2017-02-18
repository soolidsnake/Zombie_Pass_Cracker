import socket
import select
import os
import sys
import time
import tqdm
from threading import Thread


pbar = None

clients_info=[]
# combi_and_client : It is a dictionary that each key is a client, and each element is a combination. This dictionary
# will contain all the clients that are already working on a combination. """
combi_and_client = {}

#Accepts a client connection
def accept_connection(main_connection, per_time, initial_hash):
	#A thread that accepts clients and send them parameters "per_time" && "initial_hash"

	global clients_info
	while True:
		client, address = main_connection.accept()
		print("\n\t[*]A client has just connected\n")
		client.settimeout(5)
		client.send(per_time.encode())
		client.recv(1024)
		client.send(initial_hash.encode())
		try:
			clients_info.append(client)
		except socket.error:
			continue


def combi_manager(combi_list, client): 
	"""Gives the client the right combination."""
	global combi_and_client
	global pbar

	# If the client already exist in the 'combi_and_client' dictionary (doc of the variable in the beginning of the
	# script), we associate him to another combination. Then that combination is romeved from the list and returned.

	pbar.update()

	if client in combi_and_client.values():
		del combi_and_client[client]
		combi_and_client[client] = "".join(combi_list[0])
		del combi_list[0]
		return combi_and_client[client]
	else:
		combi_and_client[client] = "".join(combi_list[0])
		del combi_list[0]
		return combi_and_client[client]


def combi_partitioner(combi_list, string_length, per_time): 
	#Fills the list "combi_list" example : 
	#per_time = 2 , string_length = 3
	#combi_list = ["aaa", "aac", "aae", ...]

	string = ['a'] * string_length

	total_combin = 26 ** string_length # WILL CHANGE WHEN WE THE MASK #################################################### IMPORTANT

	combi_list.append(list(string))


	pbar = tqdm.tqdm(total = total_combin)

	while(1):

		i = 0
		while(i < per_time):
			error = next_string_rec(string, string_length -1)
			if (error == -1):
				pbar.close()
				return(-1)
			i += 1
		combi_list.append(list(string))
		pbar.update(per_time)
	

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

	global pbar

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

	per_time = input("Enter per_time number : ")
	initial_hash = input("Enter initial_hash : ")
	string_length = int(input("Enter string_length : "))
	os.system('clear')

	print("\n\n[+] Initialisation of combinations list")
	combi_partitioner(combi_list, string_length, int(per_time))
	
	os.system('clear')
	print("\n\n[+] Cracking the hash ...\n\n")
	pbar = tqdm.tqdm(total = len(combi_list))

	accept_connec_th = Thread(target=accept_connection, args=(main_connection, per_time, initial_hash), daemon=True)
	accept_connec_th.start()

	#Main Loop
	#print(combi_list)
	#print("before loop")
	while(1):
		try:
			readable, writeable, exceptional = select.select(clients_info,[] ,[] ,0)

			for readable_sock in readable:
				msg = readable_sock.recv(1024)
				#print(msg.decode())
				if(msg.decode() == "FOUND"):
					readable_sock.send(b"ok")
					print("Data found\n")
					sys.exit(0)
				else:
					if(len(combi_list) == 0):
						raise IndexError
					starting_str = combi_manager(combi_list, readable_sock)
					readable_sock.send(starting_str.encode())
				readable.remove(readable_sock)
		except socket.error:
			#If an error happens remove the client from dictonnary and from clients_info

			combi_list.append(combi_and_client[readable_sock])
			del combi_and_client[readable_sock]

			print("\n\t[*]A client has just disconnected\n")
			clients_info.remove(readable_sock)
		except IndexError:
			break

	#Cleaning all sockets
	for sock in clients_info:
		sock.close()
	main_connection.close()

if __name__ == "__main__":
	main()
