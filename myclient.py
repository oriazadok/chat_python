import socket
import threading

client = socket.socket()
PORT = 5050
SERVER_ADDRESS = "127.0.0.1"
ADDR = (SERVER_ADDRESS, PORT)
name = ""
onlineClients = []

udpClinetSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
PROTOCOL:
Private message: <p><name><to><message>
Public message: <g><message>
List of users: <u>
List of files: <f>
Download: <d><file_name>
Proceed: <r>

"""

def printMenu():
    print("Menu: ")
    print("\t 1. to log in type \"login\"")
    print("\t 2. to log out type \"logout\"")
    print("\t 3. to send private message type \"private\"")
    print("\t 4. to send global message in type \"global\"")
    print("\t 5. to get a list of online members type \"online\"")
    print("\t 6. to get a list of files type \"files\"")
    print("\t 7. to download a file type \"download\"")

    print("\t 8. to log in type \"proceed\"")

    print("\t 9. to change type \"change\"")

    print("pick an option: ")

def logIn():
    client.connect(ADDR)
    print("Insert Your name: ")
    global name
    name = input()
    client.send(name.encode())
    print("logging in")
def logOut():
    logout = True
    client.close()

def sendToOtherClient():
    getOnlineUsers()
    print("pick a friend to chat with: ")
    to = input()
    if(to not in onlineClients):
        print("no such name in the chat, please try again")
        sendToOtherClient()
    print("to change a friend to chat with type \"swap\"")
    print(f"send message for {to}")
    while True:
        msg = input()
        if(msg == ""):
            continue
        if (msg == "change"):
            print("getting out of private")
            break
        if(msg == "swap"):
            getOnlineUsers()
            print("pick a friend to chat with: ")
            to = input()
            if (to not in onlineClients):
                print("no such name in the chat, please try again")
                sendToOtherClient()
            continue
        msg = ("<p><" + name + "><" + to + "><" + msg + ">").encode()
        client.send(msg)
    print()
    printMenu()
def sendEveryone():
    print("send message for everyone")
    while True:
        msg = input()
        if (msg == ""):
            continue
        if (msg == "change"):
            print("getting out of global")
            break

        msg = ("<g><" + name + "><" + msg + ">").encode()
        client.send(msg)

    print()
    printMenu()

def getOnlineUsers():
    msg = "<u>".encode()
    client.send(msg)
def getFilesList():
    msg = "<f>".encode()
    client.send(msg)


def downloadRequest():
    getFilesList()
    print("pick a file to download: ")
    while True:
        file = input()
        if (file == "change"):
            break
        msg = ("<d><" + name + "><" + file + ">").encode()
        # client.send(msg)
        # udpClinetSocket.sendto(msg, ("127.0.0.1", 5051))
        # udpClinetSocket.sendto("check".encode(), ("127.0.0.1", 5051))

# def downloadFile():
#     msg = "<r>".encode()
#     client.send(msg)


def sendMessage():
    printMenu()
    while True:
        str = input()
        if (str == "login"):
            logIn()
            continue
        if (str == "logout"):
            logOut()
            if (logout == True):
                print("break number 2")
                break

        if (str == "global"):
            sendEveryone()
            continue
        if (str == "private"):
            sendToOtherClient()
            continue

        if (str == "online"):
            getOnlineUsers()
            continue
        if (str == "files"):
            getFilesList()
            continue

        if (str == "download"):
            downloadRequest()
            continue

        else:
            print("please try again, and check for no extra spaces")

logout = False
t = threading.Thread(target=sendMessage)
t.start()

# def getFiles():
#     while True:
#         if (logout == True):
#             print("break")
#             break
#         try:
#
#             # if(recv[1:3] == "rf"):
#             #     recv = recv[4:]
#             #     with open("new_file_2.txt", "w+") as f:
#             #         f.write(recv)
#             #     f.close()
#             #     continue
#             print("in udp")
#             udprecv = udpClinetSocket.recvfrom(1024)
#             print(udprecv[0].decode())
#         except:
#             pass
#
# u = threading.Thread(target=getFiles)
# u.start()


while True:
    if (logout == True):
        print("break")
        break
    try:
        recv = client.recv(1024).decode()
        if("---online users names---\n" in recv):
            l = recv.split("\n")[1].split(", ")
            onlineClients = l
        print(recv)
    except:
        pass

    try:
        udprecv = udpClinetSocket.recvfrom(1024)
        # print(udprecv[0].decode())


    except:
        pass
