class Person:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.username = None

    def __eq__(self, other):
        return (isinstance(other, Person) and (self.conn, self.addr) == other)

    def __str__(self):
        return f"{self.conn}: {self.addr}"

    def __repr__(self):
        return f"{self.conn}:{self.addr}"