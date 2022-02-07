import pytest
from src.server.server import Server

def test_init_server():
    """test server initialization"""
    server = Server("localhost", 8000)

def test_server_start():
    """test server start"""
    server = Server("localhost", 8000)
    server.start()