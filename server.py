import os 
from dotenv import load_dotenv 

load_dotenv()
from opt.src.server.server import Server


HOST = os.environ.get("HOST")
PORT = int(os.environ.get("PORT"))
if __name__ == "__main__":
    server = Server(host=HOST, port=PORT)
    server.start()
    # server.join()