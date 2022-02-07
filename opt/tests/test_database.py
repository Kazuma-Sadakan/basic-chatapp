import time
import pytest 
from src.database import ClientDB, MessageDB

def test_create_clientdb():
    client_db = ClientDB("test_client.db")
    client_db.create_table()

def test_save_client():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    success = client_db.save("Jack", time.time())
    assert success == True

def test_get_by_username():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    data = client_db.get_by_username("Jack")
    assert data["id"] == 1

def test_delete():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    id = client_db.get_by_username("Jack")["id"]
    success = client_db.delete(id)
    assert success == True

def test_get_client():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    client_db.save("Mike", time.time())
    id = client_db.get_by_username("Mike")["id"]
    data = client_db.get(id)
    assert "Mike" == data["username"]
    client_db.delete(id)

def test_get_all():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    client_db.save("Mike", time.time())
    client_db.save("Ben", time.time())
    client_list  = client_db.get_all()
    print('[*]', client_list)
    for client in client_list:
        client_db.delete(client["id"])

def test_update():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    client_db.save("Jack", time.time())
    id = client_db.get_by_username("Jack")["id"]
    success = client_db.update(id, username = "Dan")
    assert success == True
    data = client_db.get(client_db.get_by_username("Dan")["id"])
    assert id == data["id"]
    client_db.delete(id)
    
def test_delete_all():
    client_db = ClientDB("test_client.db")
    client_db.create_table()
    success = client_db.delete_all()
    assert success == True

def test_create_message_db():
    message_db = MessageDB("test_message.db")
    message_db.create_table()

def test_save_message():
    message_db = MessageDB("test_message.db")
    message_db.create_table()

    client_db = ClientDB("test_client.db")
    client_db.create_table()
    client_db.save("Dean", time.time())
    id = client_db.get_by_username("Dean")["id"]
    success = message_db.save(id, "hello world", time.time())
    assert success == True  

def test_get_message():
    message_db = MessageDB("test_message.db")
    message_db.create_table()
    data = message_db.get()

def test_get_message_by_client_id():
    message_db = MessageDB("test_message.db")
    message_db.create_table()

    client_db = ClientDB("test_client.db")
    client_db.create_table()
    client_db.save("Sam", time.time())
    id = client_db.get_by_username("Sam")["id"]
    success = message_db.save(id, "good night world", time.time())
    message = message_db.get_by_id(id)[0]["msg"]
    assert message == "good night world"