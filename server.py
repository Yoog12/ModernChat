#!/usr/bin/env python3
#
#
#   SERVER
#
#

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_inc_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s est connecté." % client_address)
        client.send(bytes("Bienvenue dans ModernChat !", "utf8"))
        client.send(bytes("Entrez votre pseudo et tapez entrer", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    name = client.recv(buff_size).decode()
    welcome = 'Bienvenue %s' % name
    client.send(bytes(welcome, "utf8"))
    client.send(bytes("Si vous souhaitez quitter tapez !quit", "utf8"))
    msg = "%s a rejoint le chat !" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        msg = client.recv(buff_size)
        if msg != bytes("!quit", "utf8"):
            broadcast(msg, name+": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s a quitter le chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8",)+msg)

clients = {}
addresses = {}

host = ''
port = 33000
buff_size = 1024
addr = (host, port)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(addr)


if __name__ == '__main__':
    SERVER.listen(5)
    print("En attente de connexion...")
    ACCEPT_THREAD = Thread(target=accept_inc_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()