import socket
import select
import threading

SERVER_ADDRESS = "127.0.0.1"
PORT = 5050

class Server:
    def __init__(self, addr, port) -> None:
        self.addr = addr
        self.port = port

        self.server = socket.socket()
        self.server.bind((self.addr, self.port))
        self.server.listen(10)

        self.clients = [self.server]
        self.names = ["server"]

        receive_requests_thread = threading.Thread(target=self.receive_request)
        receive_requests_thread.start()
        print("starting server..")

    def sendAll(self, name, msg, dontSend):
        for client in self.clients:
            if client not in dontSend:
                client.send(f"{name}: {msg}\n".encode())

    def sendPrivate(self, name, to, msg):
        index = self.names.index(to)
        c = self.clients[index]
        c.send(f"[private] {name}: {msg}".encode())

    def sendUsersList(self, client):
        s = "---online users names---\n"
        str = ""
        for name in self.names:
            str += name + ", "
        str = s + str[8:len(str) - 2] + "\n"
        str += "------------------------"
        client.send(str.encode())

    def analyzeRequest(self, data, dontsend):
        
        if(data[1] == 'g'):
            data = data[4:]
            name = data[:data.find(">")]
            msg = data[data.find(">") + 2:len(data) - 1]
            self.sendAll(name, msg, dontsend)
            return
        if (data[1] == "p"):
            data = data[4:]
            name = data[:data.find(">")]
            data = data[data.find(">") + 2:]
            to = data[:data.find(">")]
            msg = data[data.find(">") + 2:len(data) - 1]
            self.sendPrivate(name, to, msg)
            return
        if (data[1] == "u"):
            self.sendUsersList(dontsend[1])
            return
    
    def receive_request(self):
        
        while self.clients:
            self.active, _, _ = select.select(self.clients, [], [])
            for i in self.active:
                if i is self.server:
                    client, address = self.server.accept()
                    self.clients.append(client)

                    name = client.recv(1024).decode()
                    self.names.append(name)

                    print("connected to new client")

                    res = "hello " + name + ", wellcome to the chat!\n"
                    client.send(res.encode())
                    self.sendAll(name, "Hello friends, I just joined the chat!", [self.server, client])

                else:
                    try:
                        data = i.recv(1024).decode()
                        self.analyzeRequest(data, [self.server, i])

                    except Exception as e:
                        print(e)
                        client_index = self.clients.index(i)
                        client_name = self.names[client_index]
                        self.names.pop(self.clients.index(i))
                        self.clients.remove(i)
                        self.sendAll(client_name, "Goodbye friens, I left the chat", [self.server])
                        i.close()


server = Server(SERVER_ADDRESS, PORT)