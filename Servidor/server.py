#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee
from models import User, Game
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import threading
import time
import hashlib

class ServerThread(threading.Thread):
    def __init__(self, host="localhost", port=8000):
         threading.Thread.__init__(self)
         self.host = host
         self.port = port
         self.localServer = SimpleXMLRPCServer((self.host, self.port), allow_none=True)
    def add_function(self, function):
         self.localServer.register_function(function, function.__name__)

    def run(self):
        self.localServer.serve_forever()


connected = {}

def user_login(username, password, ip, port):
    global connected
    response = {'success': False}
    try:
        user = User.select().where(User.username == username)
        if User.get(User.username == username).password == password:
            response = {'success': True, "message": "Bienvenido {0}".format(username)}
            connected[username] = {"connection": (ip, port), "state": "waiting"}
        else:
            response["message"] = u"password o usuario incorrectos"
    except peewee.DoesNotExist as e:
        response["errors"] = (str(e))
    return response

def get_connected_users():
    global connected
    return connected

def retrieve_list():
    global connected
    users = [k for k, v in connected.items() if v["state"] == "waiting"]
    return users

def user_create(username,name, email, password):
    response = {'success': False}
    data = {}
    data["username"] = username
    data["name"] = name
    data["email"] = email
    data["password"] = password
    try:
        user = User.create(**data)
        print(user)
        response = {'success': True, "message": "The User was created"}
    except peewee.IntegrityError as e:
        response["errors"] = (str(e))
    return response

def update_list():
    global connected
    connected_users = retrieve_list()
    for k, v in connected.items():
        ip, port = connected[k]["connection"]
        client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))
        client.update_list(connected_users) # call to player's server

def user_logout(username):
    global connected
    response = {'success': False}
    try:
        ip, port = connected[username]["connection"]
        del(connected[username])
        client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))
        print("Deleting user:", username)
        response = {'success': True, "message": "Usuario deslogeado"}
        update_list()
    except NameError as e:
        response["errors"] = (str(e))
    return response


def update_state(username, state):
    global connected
    connected[username]["state"] = state
    update_list()

def update_state_and_start_game(username, opponent):
    global connected
    connected[username]["state"] = "ready"
    print(connected)
    if connected[opponent]["state"] == "ready":
        print("username: {} opponent: {}".format(username, opponent))

        ip_opponent, port_opponent = connected[opponent]["connection"]
        client_username = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip_opponent, port_opponent))
        opponent_map = client_username.get_map()
        print("opponent_map",opponent_map)

        ip_username, port_username = connected[username]["connection"]
        client_opponent = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip_username, port_username))
        username_map = client_opponent.get_map()

        client_opponent.set_map(opponent_map)
        client_username.set_map(username_map)

        # Activate the username's board
        client_opponent.activate_board(True)


def start_battle(username, opponent):
    global connected
    ip, port = connected[opponent]["connection"]
    print("IP opponent:", ip, opponent)
    client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))
    client.start_battle(opponent, username)

def send_info_to_opponent(opponent, cell):
    ip, port = connected[opponent]["connection"]
    client = xmlrpc.client.ServerProxy("http://{0}:{1}".format(ip, port))
    client.received_shoot(cell)
    client.activate_board(True)

def save_game(username, opponent1):
    esponse = {'success': False}
    winner = username
    opponent = opponent1
    fecha = time.strftime("%d/%m/%y")
    try:
        game = Game.create(winner=winner, opponent=opponent, fecha=fecha)
        #print(game)
        response = {'success': True, "message": "The User was created"}
    except peewee.IntegrityError as e:
        response["errors"] = (str(e))
    return response

# def get_games(username):
#     response={}
#     for i in [1,2,3,4,5,6,7,8,9,10]:
#         try:
#             game = Game.select().where(Game.id==i)
#             if Game.get(Game.winer == username or Game.winner == username):
#                 response = {'success': True, "message": "Bienvenido {0}".format(username)}
#                 connected[username] = {"connection": (ip, port), "state": "waiting"}
#             else:
#                 response["message"] = u"password o usuario incorrectos"
#         except peewee.DoesNotExist as e:
#             response["errors"] = (str(e))
#     return response



if __name__ == '__main__':
    functions = [user_login, get_connected_users, retrieve_list, user_logout,
                 user_create, update_state, update_list, start_battle,
                 update_state_and_start_game, send_info_to_opponent, save_game]

    server = ServerThread()

    for function in functions:
        server.add_function(function)

    server.start()

    print("Servidor corriendo en {0}:{1}".format(server.host, server.port))
    #
    # password = hashlib.sha256("sasuke93".encode()).hexdigest()
    # client = xmlrpc.client.ServerProxy("http://localhost:8000/")
    # response = client.user_login("oca159", password, "localhost", 8001)
    # print(response)
    # response = client.get_connected_users()
    # print(response)
    # response = client.retrieve_list("susana")
    # print(response)
    # response = client.user_logout("susana")
    # print(response)
    # response = client.get_connected_users()
    # print(response)
    # password = hashlib.sha256("sasuke93".encode()).hexdigest()
    # response = client.user_create("mario", "mario", "mario@mario.com",password)
    # print(response)
