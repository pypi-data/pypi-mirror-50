import __init__ as easystreaming, hashlib
server = easystreaming.ServerStream("127.0.0.1", 1332, 10)
server.connect()
def rcv(sock, data):
    print(str(hash(sock)) + " : " + str(data))
    sock.send(data)
server.setListener("recv", rcv)
client = easystreaming.ClientStream("127.0.0.1", 1332)
client.connect()
def rcv_c(_, data):
    client.send(data)
client.setListener("recv", rcv_c)
bf = hashlib.sha256(str(hash(server)).encode()).hexdigest()
client.send(bf)
server.send(0, "Hi")