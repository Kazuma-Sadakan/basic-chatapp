import pytest
from src.server.client import ClientThread

def test_init_client():
    """test server initialization"""
    server = ClientThread("localhost", 8000)

def test_server_start():
    """test server start"""
    server = ClientThread("localhost", 8000)
    server.start()