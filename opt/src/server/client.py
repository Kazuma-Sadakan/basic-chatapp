import os
import sys
import time
import struct
import socket 
import threading, queue
from enum import Enum
import logging
import errno
from dotenv import load_dotenv

from opt.src.utils.utils import decode, encode, pickle_load, pickle_dumps

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
LOGGING_FILE = os.path.join(BASE_DIR, "client.log")
logging.basicConfig(filename = LOGGING_FILE, level = logging.DEBUG, 
                    format = "%(asctime)s:%(levelname)s:%(message)s")

# from ..utils import create_message
def create_message(sender, msg):
    return {
            "sender": sender,
            "text": msg
        }


# Connection Data
HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))
BUFFER_SIZE = int(os.environ.get("BUFFER_SIZE"))
REQUEST_SIZE = int(os.environ.get("REQUEST_SIZE"))
BYTE_SIZE = struct.calcsize("<L")

class Controller(Enum):
    CONNECT =  0
    SEND = 1
    RECEIVE = 2
    CLOSE = 3

class ClientThread(threading.Thread):
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.address = (host, port)
        self.alive = threading.Event()
        self.alive.set()
        self.q = queue.Queue() 
        self.msg_q = queue.Queue()
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):      
        print("client", self.alive.is_set())
        while self.alive.is_set():
            try:
                crl, data = self.q.get(True, 0.1)
                if crl == Controller.CONNECT:
                    self._connect(data)
                elif crl == Controller.RECEIVE:
                    msg = self._receive()
                    self.msg_q.put(msg)
                elif crl == Controller.SEND:
                    self._send(data)
                elif crl == Controller.CLOSE:
                    self._close()
            except queue.Empty as e:
                print(e)
                continue

    def controller(self, crl, data):
        self.q.put((crl, data)) 
    
    def _connect(self, data):
        try:
            self.name = data
            self.soc.connect(self.address)
            logging.info("connected to the chatroom...")
        except IOError as e:
            if e.errno == errno.EPIPE:
                logging.error(e)
                self._send("[DISCONNECT]")
                sys.exit(1)

    def _recv(self):
        while self.alive.is_set():
            try:
                bmsg_size = self.soc.recv(BYTE_SIZE)
                bmsg_size = struct.unpack("<L", bmsg_size)[0]
                bmsg = bytes()
                while len(bmsg) < bmsg_size:
                    bmsg += self.soc.recv(bmsg_size)
            except IOError as e:
                if e.errno == errno.EPIPE:
                    logging.error(e)
                    sys.exit(1)
            return pickle_load(bmsg)

    def _send(self, msg):
        msg = {
            "sender": self.name,
            "message": msg,
            "timestamp": time.time()
        }
        bmsg = pickle_dumps(msg)
        data = struct.pack("<L", len(bmsg)) + bmsg
        try:
            self.soc.sendall(data)
        except IOError as e:
            if e.errno == errno.EPIPE:
                logging.critical(e)
                sys.exit(1)

    def close(self):
        self._send("[DISCONNECT]")
        self.soc.close()
        
    def join(self):
        self.alive.clear()
        self.soc.close()
        threading.Thread.join(self)  


