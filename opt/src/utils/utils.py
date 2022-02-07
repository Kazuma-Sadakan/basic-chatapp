import pickle

def decode(data:str):
    return data.decode()

def encode(data:str):
    return data.encode()

def pickle_load(data:bytes):
    return pickle.loads(data)

def pickle_dumps(data:dict):
    return pickle.dumps(data)


def create_message(sender, msg, timestamp):
    return {
            "sender": sender,
            "text": msg,
            "timestamp": timestamp
        }

