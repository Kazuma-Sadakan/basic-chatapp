from cmath import log
import logging
import sqlite3
import os 
basedir  = os.path.abspath(os.path.dirname(__file__))

import os, time
import datetime
import sqlite3

BASE_URL = os.path.dirname(__file__)

def time_converter(timestamp):
    return str(datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"))

class Database:
    def __init__(self, db_name:str):
        db_path = os.path.join(BASE_URL, db_name)
        if not os.path.isfile(db_path):
            open(db_path, mode="w").close()
            print(f"[*] Database {db_path} created...")
        try:
            self.connect = sqlite3.connect(db_path)
            self.cursor = self.connect.cursor()
            print(f"[*] Connected to {db_name}")

        except:
            print("Connecting to the database failed...")

        

    def create_table(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def update(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        raise NotImplementedError

    def get(self, *args, **kwargs):
        raise NotImplementedError

    def dump_cursor(self):
        self.cursor.close()
        
    def close(self):
        self.connect.close()


class ClientDB(Database):
    def __init__(self, db_name):
        super().__init__(db_name)

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS client
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username text NOT NULL UNIQUE, 
            timestamp text NOT NULL) 
        """)
        self.connect.commit()

    def save(self, username:str, timestamp:str = time.time()):
        timestamp = time_converter(timestamp)
        try:
            self.cursor.execute("""
                INSERT INTO client (username, timestamp) VALUES (:username, :timestamp)
            """, {"username": username, "timestamp": timestamp})
            self.connect.commit()
            return True 
        except Exception as e:
            logging.error(e)
            return False 

    def update(self, id:int, username:str) -> bool:
        try:
            self.cursor.execute("""
                UPDATE client SET username = :username WHERE id = :id
            """, {"id": id, "username": username})
            self.connect.commit()
            return True
        except Exception as e:
            logging.error("client updates failed")
            print(e)
            return False

    def delete(self, id:int) -> bool:
        try:
            self.cursor.execute("""
                DELETE from client WHERE id = :id
            """, {"id": id})
            self.connect.commit()
            return True
        except Exception as e:
            logging.error("client delete failed")
            return False

    def get(self, id:int) -> dict:
        try:
            self.cursor.execute("""
                SELECT id, username, timestamp FROM client WHERE id = :id
            """, {"id": id})
            client = self.cursor.fetchone()
            if client is None:
                return {}
            return {"id": client[0], "username": client[1], "timestamp": client[2]}
        except Exception as e:
            logging.error(e)
            return {}

    def get_all(self) -> list:
        try:
            self.cursor.execute("""
                SELECT id, username, timestamp FROM client
            """)
            client_list = self.cursor.fetchall()
            if not bool(client_list):
                return []
            return [{"id": client[0], "username": client[1], "timestamp": client[2]}for client in client_list]
        except Exception as e:
            logging.error(e)
            return []

    def get_by_username(self, username:str) -> dict:
        try:
            self.cursor.execute("""
                SELECT id, username, timestamp FROM client WHERE username = :username
            """, {"username": username})
            client = self.cursor.fetchone()
            if client is None:
                return {}
            return {"id": client[0],
                    "username": client[1], 
                    "timestamp": client[2]}
        except Exception as e:
            logging.error(e)
            return {}

    def delete_all(self) -> bool:
        try:
            self.cursor.execute("""
                DELETE from client
            """)
            self.connect.commit()
            return True
        except Exception as e:
            logging.error("client delete failed")
            return False

class MessageDB(Database):
    def __init__(self, db_name:str):
        super().__init__(db_name)
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
            msg TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            client_id INTEGER NOT NULL, 
            FOREIGN KEY (client_id) REFERENCES client(client_id)
                ON UPDATE CASCADE
                ON DELETE CASCADE
            )
        """)
        self.connect.commit()

    def save(self, client_id:int, message:str, timestamp:str) -> bool:
        try:
            timestamp = time_converter(timestamp)
            self.cursor.execute("""
                INSERT INTO messages (msg, client_id, timestamp) VALUES (:msg, :client_id, :timestamp)
            """, {"msg": message, 'client_id': client_id, "timestamp": timestamp})
            self.connect.commit()
            return True
        except Exception as e:
            logging.error(e)
            return False

    def get(self) -> dict:
        try:
            self.cursor.execute("""
                SELECT msg, timestamp FROM messages
            """)
            message_list = self.cursor.fetchall()
            if not bool(message_list):
                return []
            return [{"msg": message[0], "timestamp": message[1]} for message in message_list]
        except Exception as e:
            logging.error(e)
            return []

    def get_by_id(self, client_id:int) -> list:
        try:
            self.cursor.execute("""
                SELECT msg, timestamp FROM messages WHERE client_id = :client_id ORDER BY timestamp
            """, {"client_id": client_id})
            message_list = self.cursor.fetchall()
            if not bool(message_list):
                return []
            return [{"msg": data[0], "timestamp": data[1]} for data in message_list]
        except Exception as e:
            logging.error(e)
            return []

    def get_all(self) -> list:
        try:
            self.cursor.execute("""
                SELECT msg, timestamp FROM messages ORDER BY timestamp
            """)
            message_list = self.cursor.fetchall()
            if not bool(message_list):
                return []
            return [{"msg": data[0], "timestamp": data[1]} for data in message_list]
        except Exception as e:
            logging.error(e)
            return []
        


