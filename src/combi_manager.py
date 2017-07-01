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

combi_list = []
combi_and_client = {}
pbar = None


def init_pbar():
    global pbar
    pbar = tqdm.tqdm(total = len(combi_list))


def give_combination(client):
    """This function return the right combination to give to the 'client', and keep track of which client is 
    having which combination (within the dictionary 'combi_and_client')."""

    # If the client already exist in the 'combi_and_client' dictionary (doc of the variable in the beginning of the
    # script), we associate him to another combination. Then that combination is romeved from the list and returned.

    global pbar
    global combi_and_client
    global combi_list

    pbar.update()

    if client in combi_and_client:
        del combi_and_client[client]

    combi_and_client[client] = combi_list[0]
    del combi_list[0]
    # print(combi_list[:10])
    return combi_and_client[client]


def disconnected_client(client):
    """This method return all the unfinished combinations of the disconnected client, into the list 
    'combi_list' (to not loose combinations when a client disconnect). """
    pass
