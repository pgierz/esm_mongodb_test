#!/usr/bin/env python3
# coding: utf-8
"""
Generates a new database in the AWI MongoDB server. Prints out all the database
names found on the server, if it is reachable, otherwise, informs you that the
server cannot be found.

Usage
-----
Simple usage as a script::
    $ python create_esm_database.py

Otherwise, you can ``pip install`` this package with::
    $ pip install git+https://github.com/pgierz/esm_mongodb_test

And then create a new database with::
    $ esm_database_create <db_name>
"""
import datetime
import getpass
import hashlib
from urllib.parse import quote_plus
from typing import Union

import click
from pymongo.database import Database
from pymongo.errors import ConnectionFailure
from pymongo.mongo_client import MongoClient

HOST: str = "bhv-mongodb.awi.de"
"""str: the database hostname"""
USER: str = "myUserAdmin"
"""str: the admin user"""
PASSWORD: str = "chooP3ai"
"""str: the admin password
WARNING(PG): I need to find a better way of doing this, hard coding it is silly...
"""
URI: str = "mongodb://%s:%s@%s" % (quote_plus(USER), quote_plus(PASSWORD), HOST)
"""str: The canonical connection string for pymongo"""

URI_WITHOUT_AUTH: str = "mongodb://%s" % (HOST)
"""str: Just the host connection, without logging in as admin"""


def check_server():
    with MongoClient(URI) as client:
        try:
            rvalue = client.admin.command("ping")
            print(f"Server {HOST} was found, we got back from ping ---> {rvalue}")
        except ConnectionFailure as e:
            print(f"Server {HOST} not available")
            raise e


@click.version_option()
@click.group()
def main(args=None):
    return 0


@main.command
def lsdb() -> list[str]:
    check_server()
    with MongoClient(URI) as client:
        db_names = client.list_database_names()
        print(f"{HOST} has {len(db_names)} databases:")
        [print(db_name) for db_name in db_names]
        return db_names


@main.command
@click.argument("db_name")
def mkdb(db_name: str) -> Union[Database, None]:
    """
    Generates a new database on MongoDB.

    Returns
    -------
    db : ~pymongo.database.Database
    """
    check_server()
    with MongoClient(URI) as client:
        print(f"Creating {db_name} on {HOST}")
        db = client[db_name]
        collection = db["simulations"]
        config = {"name": "example"}
        m = hashlib.sha256()
        m.update(f"{config}_{getpass.getuser()}_{datetime.datetime.now()}".encode('utf-8'))
        config["hash"] = m.hexdigest()
        collection.insert_one(config)
        print("From the database -->")
        print(collection.find_one())
        return db



@main.command
@click.argument("db_name")
def rmdb(db_name: str) -> None:
    check_server()
    with MongoClient(URI) as client:
        print(f"Removing {db_name}")
        client.drop_database(db_name)


if __name__ == "__main__":
    main()
