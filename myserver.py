import socket
import select
# from udpRdtSocket import RUDP


server = socket.socket()
PORT = 5050
SERVERADDRESS = "127.0.0.1"
ADDR = (SERVERADDRESS, PORT)
server.bind(ADDR)
server.listen(10)

udpServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpServerSocket.bind(("127.0.0.1", 5051))

clients = [server]
udpClients = []
names = ["server"]
files = ["file_1.txt, file_2.txt"]
# files = []
print("starting server..")

def sendAll(name, msg, dontSend):
    for client in clients:
        if client not in dontSend:
            client.send(f"(global message) {name}: {msg}".encode())
def sendPrivate(name, to, msg):
    index = names.index(to)
    c = clients[index]
    c.send(f"(private message) {name}: {msg}".encode())

def sendUsersList():
    s = "---online users names---\n"
    str = ""
    for name in names:
        str += name + ", "
    str = s + str[8:len(str) - 2] + "\n"
    str += "------------------------"
    i.send(str.encode())

def sendFilesList():
    i.send("---files in the server---".encode())
    if not (files):
        i.send("no files in the server\n".encode())
    else:
        str = ""
        for file in files:
            str += file + ", "
        str = str[:len(str) - 2] + "\n"
        i.send(str.encode())
    i.send("-------------------------".encode())



def sendFile(name, filename):
    print(f"name: {name}, filename: {filename}")


    # udpclientMsg, udpaddress = udpServerSocket.recvfrom(1024)
    # udpClients.append(udpaddress)
    # print(udpclientMsg)
    # print(udpClients)

    # urs = RUDP()

    # index = names.index(name)
    # cAddr = clients[index].getpeername()
    # print(cAddr)

    # print(udpClients[0])
    # udpServerSocket.sendto("hello from udp".encode(), udpClients[0])
    # print("sendddddddddddd")

    # f = open(filename)
    # outputdata = f.read()

    ##########  OBJ ##############################
    # urs.send(f"<rf>{outputdata}".encode(), cAddr)
    # urs.send("<rf>{outputdata}".encode(), cAddr)
    # urs.close()
    ##########################################

    # f.close()
def proceed():
    pass


def analyzeRequest(data, t):
    
    if(data[1] == 'g'):
        data = data[4:]
        name = data[:data.find(">")]
        print(f"name: {name}")
        msg = data[data.find(">") + 2:len(data) - 1]
        print(f"msg: {msg}")
        sendAll(name, msg, t)
        return
    if (data[1] == "p"):
        data = data[4:]
        name = data[:data.find(">")]
        data = data[data.find(">") + 2:]
        to = data[:data.find(">")]
        msg = data[data.find(">") + 2:len(data) - 1]
        sendPrivate(name, to, msg)
        return
    if (data[1] == "u"):
        sendUsersList()
        return
    if (data[1] == "f"):
        sendFilesList()
        return

    if (data[1] == "d"):
        data = data[4:]
        name = data[:data.find(">")]
        data = data[data.find(">") + 2:]
        filename = data[:len(data) - 1]
        sendFile(name, filename)
        return
    if (data[1] == "r"):
        proceed()

while clients:
    active, _, _ = select.select(clients, [], [])
    for i in active:
        if i is server:
            client, address = server.accept()
            clients.append(client)
            name = client.recv(1024)
            names.append(name.decode())
            print("connected to new client")

            # udpclientMsg, udpaddress = udpServerSocket.recvfrom(1024)
            # udpClients.append(udpaddress)
            # print(udpclientMsg)
            # print(udpClients)

            res = "hello " + name.decode() + ", wellcome to the chat!"
            client.send(res.encode())
            sendAll("", f"{name.decode()} enterd the chat", [server, client])

        else:
            try:
                data = i.recv(1024)
                analyzeRequest(data.decode(), [server, i])

            except Exception as e:
                print(e)
                n = names[clients.index(i)]
                names.pop(clients.index(i))
                clients.remove(i)
                sendAll("", f"{n} left the chat".encode(), [server])
                i.close()