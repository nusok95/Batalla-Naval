from peewee import *
import json

db = MySQLDatabase("battleship", user="battleship", passwd="camilo14", host="localhost", port=3306)

class Ship(Model):
    x = CharField()
    y = CharField()

    class Meta:
        database = db # This model uses the "people.db" database.

# mas modelos

class User(Model):
    name = CharField()
    email = CharField(unique=True)
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class Game(Model):
    winner=CharField()
    opponent=CharField()
    fecha=CharField()

    class Meta:
        database = db


db.connect()

tables = [Ship, User, Game]
#db.drop_tables(tables)
db.create_tables(tables,safe=True)