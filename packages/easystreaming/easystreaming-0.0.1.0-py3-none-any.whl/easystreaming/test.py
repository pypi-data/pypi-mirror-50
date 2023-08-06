import __init__ as easystreaming, hashlib
server = easystreaming.ServerStream("127.0.0.1", 1332, 10)
server.connect()
def rcv(sock, data):
    print(str(hash(sock)) + " : " + data)
server.setListener("recv", rcv)
client = easystreaming.ClientStream("127.0.0.1", 1332)
client.connect()
bf = hashlib.sha256(str(hash(server)).encode()).hexdigest()
while True:
    bf = hashlib.sha256(bf.encode()).hexdigest()
    client.send(bf)