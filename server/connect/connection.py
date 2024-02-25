import os
import sys
import json
import socket
import logging

from sqlmodel import SQLModel, Session, create_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, '../../config.json')
CONFIG = json.loads(open(FILE_PATH).read())

db = CONFIG["DATABASE_INFORMATION"]

DATABASE_URL = f"mysql+pymysql://" \
               f"{db.get('user')}" \
               f":{db.get('password')}" \
               f"@{db.get('host')}" \
               f":{db.get('port')}" \
               f"/{db.get('database')}" \
               f"?charset={db.get('charset')}"

engine_url = create_engine(DATABASE_URL,
                           echo=True,
                           # connect_args={"check_same_thread": False} # sqlite
                           )


def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def check_port(port):
    if is_port_in_use(port):
        logging.info(f"port {port} is already in use.")
        sys.exit(1)
    else:
        logging.info(f"port {port} is available.")


def make_table():
    SQLModel.metadata.create_all(bind=engine_url,
                                 checkfirst=True
                                 )


def get_session():
    with Session(engine_url) as session:
        yield session
