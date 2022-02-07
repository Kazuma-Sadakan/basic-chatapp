from opt.src import app
import argparse

parser = argparse.ArgumentParser(description = "port setting")
parser.add_argument("-p", '--port', help = "port")

if __name__ == "__main__":
    args = parser.parse_args()
    port = args.port if args.port else 8000
    app.run(debug = True, port=port)

    