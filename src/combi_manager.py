#!/usr/bin/python3

"""This module manage combinations between the clients.

Variables:
    combi_list : The total list of combinations that will be distributed on the clients.
    combi_and_client : It is a dictionary that each key is a client, and each element is a list of combinations. 
        Example : {client1: ['aaa', 'aac', 'aae'], client2: ['aag', 'aai']}
        This dictionary will contain all the clients and all the combinations that they are working on.
    pbar : Progress bar of the work.
"""

import tqdm
from collections import deque

combi_list = deque()
combi_and_client = {}
pbar = None


def init_pbar():
    global pbar
    pbar = tqdm.tqdm(total = len(combi_list))


def give_combination(client):
    """This function return the right combination to give to the 'client', and keep track of which client is 
    having which combination (within the dictionary 'combi_and_client')."""

    global combi_and_client, combi_list


    if client not in combi_and_client:
        combi_and_client[client] = []

    combi = combi_list.popleft()
    combi_and_client[client] += [combi]
    # print("Client list :", combi_and_client[client])
    client.send(combi.encode())


def finished_combination(client, combination):
    """This function is used when a client finish a combination."""

    global pbar

    pbar.update()
    combi_and_client[client].remove(combination)


def disconnected_client(client):
    """This method reput all the unfinished combinations of the disconnected client, into the list 
    'combi_list' (to not loose combinations when a client disconnect). """

    combi_list.extendleft( combi_and_client[client] )
    del combi_and_client[client]