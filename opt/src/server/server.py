import errno
import os 
import sys
import socket 
import threading 
import logging 
import struct
import time
from enum import Enum

from dotenv import load_dotenv 

from opt.src.person import Person
from opt.src.utils.utils import encode, decode, pickle_dumps, pickle_load


load_dotenv(verbose=True)
BASE_DIR = os.path.dirname(__file__)
LOGGING_FILE = os.path.join(BASE_DIR, "test.log")
BUFFER_SIZE = int(os.environ.get("BUFFER_SIZE"))
REQUEST_SIZE = int(os.environ.get("REQUEST_SIZE"))
BYTE_SIZE = struct.calcsize("<L")

logging.basicConfig(filename = LOGGING_FILE, level = logging.DEBUG, 
                    format = "%(asctime)s:%(levelname)s:%(message)s")



class State(Enum):
    CONNECT=0
    RECEIVE=1
    PROCESS=2
    SEND=3
    BROADCAST=4
    ERROR=5


class Server(threading.Thread):
    
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.alive = threading.Event()
        self.alive.set()
        self.client_list = []
        self.thread_list = []
        # Create a listening socket
        self.socket = socket.socket(Server.address_family, Server.socket_type)
        # Allow to reuse the same address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_address = (host, port)
        try:
            # Bind the socket to the port
            self.socket.bind(server_address)
        except IOError as e:
            logging.error(e)
            sys.exit(1)

        host, port = self.socket.getsockname()[:2]
        domain_name = socket.getfqdn(host)
        logging.info(f"[*] Server:{domain_name} is running on port {port}...")
        print(f"[*] Server:{domain_name} is running on port {port}...")
        
    def _listen(self):
        try:
            self.socket.listen(REQUEST_SIZE)
            logging.info(f"[*] Server starts listening...")
        except Exception as e:
            logging.critical(f"Server listening failed: {e}")
            sys.exit(1)

    def _accept(self):
        conn, addr = self.socket.accept()
        logging.info(f"{conn}:{addr} is connected")
        print(f"{conn}:{addr} is connected")
        self.lock.acquire()
        person = Person(conn = conn, addr = addr)
        self.client_list.append(person)
        self.lock.release()

        thread = threading.Thread(target=self._handle, args = (person, ))
        self.thread_list.append(thread)
        self.thread_list[-1].start()

    def run(self):
        self._listen()
        while self.alive.is_set():
            try:
                self._accept()
            except KeyboardInterrupt:
                logging.info("KeybortInterrupt. server closed...")
                self.socket.close()
                sys.exit(0)

            except Exception as e:
                logging.critical(f"Server crushed: {e}")
                self.socket.close()
                sys.exit(1)


    def _handle(self, person):
        print("server5", self.alive.is_set())
        while self.alive.is_set():
            try:
                bmsg = self._recv(person)
                print("server", pickle_load(bmsg))
            except ValueError as e:
                logging.error(e)
                response = {
                    "sender": "SERVER",
                    "message": "message cannot be empty",
                    "timestamp": time.time()
                }
                self._send(person, pickle_dumps(response))
                    
            if pickle_load(bmsg).get("message", None) == "[DISCONNECTED]":
                person.conn.close()
                self.lock.acquire()
                self.client_list.remove(person)
                self.lock.release()
            print("person", person)
            self._broadcast(person, bmsg)

    def _recv(self, person):
        try: 
            bmsg_size = struct.unpack("<L", person.conn.recv(BYTE_SIZE))[0]
            print("[*]", bmsg_size)
            if bmsg_size == 0:
                raise ValueError("msg is empty")
            bmsg = bytes()
            while len(bmsg) < bmsg_size:
                bmsg += person.conn.recv(BUFFER_SIZE)
            return bmsg
        except IOError as e:
            if e.errno == errno.EPIPE:
                logging.error(f"{person}: BROKEN PIPE")
                person.conn.close()
                self.lock.acquire()
                self.clisnt_list.remove(person)
                self.lock.release()
                return ""

    def _send(self, person, bmsg):
        data = struct.pack("<L", len(bmsg)) + bmsg
        try:
            person.conn.send(data)
        except IOError as e:
            if e.errno == errno.EPIPE:
                person.conn.close()
                self.lock.acquire()
                self.client_list.remove(person)
                self.lock.release()

    def _broadcast(self, person, msg):
        for client in self.client_list[:]:
            # if client == person: 
            #     continue
            print("client", client, "-->", msg)
            self._send(client, msg)

    def join(self):
        self.alive.clear()
        for thread in self.thread_list[:]:
            try:
                thread.join()
            except Exception as e:
                logging.error(e)
        try:
            threading.Thead(self).join()
        except Exception as e:
            logging.error(e)

        logging.info(f"[*] Server is down")
        sys.exit(0)

