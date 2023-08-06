import __init__ as easystreaming
server = easystreaming.ServerStream("127.0.0.1", 1332, 10)
server.connect()
def rcv(sock, data):
    print(hash(sock) + " : " + data)
server.setListener("recv", rcv)
client = easystreaming.ClientStream("127.0.0.1", 1332)
client.connect()
client.send("Hi")