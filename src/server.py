import socket
import select
import os
import sys
import time
import tqdm
from threading import Thread

import combi_manager


clients_info=[]


def hash_alg_list():
	"""Print list of all hashs algorithms."""

	print('\n\
			0 - SHA512\n\
			1 - MD5\n\
		 ')


#Accepts a client connection
def accept_connection(main_connection, choice, per_time, initial_hash, string_length):
	#A thread that accepts clients and send them parameters "per_time" && "initial_hash"

	global clients_info
	while True:
		client, address = main_connection.accept()
		print("\n\t[*]A client has just connected\n")
		client.settimeout(5)
		client.send(choice.encode())
		client.recv(1024)
		client.send(per_time.encode())
		client.recv(1024)
		client.send(initial_hash.encode())
		client.recv(1024)
		client.send(string_length.encode())
		try:
			clients_info.append(client)
		except socket.error:
			continue


def combi_partitioner(string_length, per_time): 
	"""Fills the list "combi_list" example : 
	per_time = 2 , string_length = 3
	combi_list = ["aaa", "aac", "aae", ...] """ 

	string = [ord('a')] * string_length

	total_combin = 26 ** string_length # WILL CHANGE WHEN WE THE MASK #################################################### IMPORTANT

	pbar = tqdm.tqdm(total = total_combin)

	combi_manager.combi_list.append("".join([chr(c) for c in string]))

	# This loop will stop when we see that we are trying to bypass 'z' on the last character of the string. 
	while True:
		step = per_time
		# Uncomment this for debugging.
		# print("".join([chr(c) for c in string]))
		# time.sleep(0.1)

		try:
			while step != 0:
				# We increment each character with the correct value.
				for i in range(-1, -string_length - 1, -1):
					string[i] = string[i] + (step % 26)

					# If we see that the current character value is bypassing 'z', then we fix the current character
					# and increment the next characters correctly.
					if string[i] > 122:
						for j in range(i, -string_length - 1, -1):
							if string[j] > 122:
								string[j] = (string[j] % 123) + 97
								string[j-1] = string[j-1] + 1
							else:
								break
					step //= 26 # We divide the step to go to the next character of the string.

		# If we are trying to increment a character in an index bigger that the string length, then we know 
		# that we finished generating all the combinations.
		except IndexError:
			break
		combi_manager.combi_list.append("".join([chr(c) for c in string]))
		pbar.update(per_time)

	return 0


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


def setting_hash_86x64(initial_hash, choice):
	s = []
	if choice == 0: #sha512
		s = '-'.join(initial_hash[i:i+16] for i in range(0, len(initial_hash), 16))
	elif choice == 1: #md5
		for i in range(0, len(initial_hash), 16):
			k = []
			k = initial_hash[i:i+16]
			m = []
			m = [k[i:i+2] for i in range(0, len(k), 2)]
			m = m[::-1]
			s.append(''.join([j for j in m]))
		s = '-'.join([j for j in s])

	return s


def main():
	os.system('clear')

	Hash_type = ""
	Hash = ""

	hash_alg_list()
	choice = input("Choose hash algorithm : ")
	per_time = input("Enter per_time number [default 100 000]: ")
	if per_time == '':
		per_time = '100000'
	initial_hash = input("Enter initial_hash : ")
	string_length = input("Enter string_length : ")
	os.system('clear')

	print("\n\n[+] Setting up the hash")
	initial_hash = setting_hash_86x64(initial_hash, int(choice))
	print(initial_hash)

	print("\n\n[+] Initialisation of combinations list")
	combi_partitioner(int(string_length), int(per_time))


	###############################################################
	main_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	main_connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # To refuse the socket if it is in time_wait
	main_connection.bind(("0.0.0.0", 12345))
	main_connection.listen(10)															  #
	###############################################################


	
	os.system('clear')
	print("\n\n[+] Cracking the hash ...\n\n")
	combi_manager.init_pbar()

	accept_connec_th = Thread(target=accept_connection, args=(main_connection, choice, per_time, initial_hash, string_length), daemon=True)
	accept_connec_th.start()

	#Main Loop
	
	while(1):
		try:
			readable, writeable, exceptional = select.select(clients_info,[] ,[] ,0.01)

			for readable_sock in readable:
				msg = readable_sock.recv(1024)

				if not readable_sock in combi_manager.combi_and_client:
					starting_str = combi_manager.give_combination(readable_sock)
					readable_sock.send(starting_str.encode())

				
				if(msg.decode() == "FOUND"):
					readable_sock.send(b"ok")
					msg = readable_sock.recv(1024)#Receive password
					print("\n\n\t[+]Password : " + msg.decode() + "\n")
					sys.exit(0)
				else:
					# This can cause a problem, because the clients are taking extra combination, and the list 
					# might be empty although the clients are still processing some combinations. Which will make the
					# server quit before all the combinations are really done.
					if(len(combi_manager.combi_list) == 0):
						raise IndexError
					starting_str = combi_manager.give_combination(readable_sock)
					readable_sock.send(starting_str.encode())
				# readable.remove(readable_sock)
		except socket.error:
			#If an error happens remove the client from dictonnary and from clients_info

			combi_manager.combi_list.append(combi_manager.combi_and_client[readable_sock])
			del combi_manager.combi_and_client[readable_sock]

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
