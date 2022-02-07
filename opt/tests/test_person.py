import pytest 
from src.person import Person

def test_create_person():
    """test person object creation"""
    person = Person("123", "234", "name")
    
