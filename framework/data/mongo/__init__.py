#!/usr/lib/env python
#-*- encoding:utf-8 -*-


from document import Document
from pymongo import MongoClient
from bson import DBRef, ObjectId


try:
    from personal import MONGODB_HOST, MONGODB_PORT, MONGODB_DB, MONGODB_URI
except:
    try:
        from settings import MONGODB_HOST, MONGODB_PORT, MONGODB_DB
    except:
        MONGODB_HOST = "127.0.0.1"
        MONGODB_PORT = 27017
        MONGODB_DB = "bots"

try:
    from personal import MONGODB_USER, MONGODB_PASSWORD
except:
    try:
        from settings import MONGODB_USER, MONGODB_PASSWORD
    except:
        MONGODB_USER = ""
        MONGODB_PASSWORD = ""


#db = MongoClient(MONGODB_HOST, MONGODB_PORT, document_class=Document)[MONGODB_DB]
db = MongoClient(MONGODB_URI, document_class=Document)[MONGODB_DB]


def database(name=MONGODB_DB, host=MONGODB_HOST, port=MONGODB_PORT):
    return MongoClient(host, port, document_class=Document)[name]


def fetch(self, db=db):
    return db.dereference(self)

DBRef.fetch = fetch


def id_fetch(self, table, db=db):
    return db.dereference(DBRef(table, self))

ObjectId.fetch = id_fetch
