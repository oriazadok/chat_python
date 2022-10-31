from optparse import Option
import socket
import threading
import tkinter
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext
from tkinter import Entry, PhotoImage, simpledialog
from turtle import width
from unicodedata import name
from unittest.main import main
import time

SERVER_ADDRESS = "127.0.0.1"
PORT = 5050

class Client:

    """
    PROTOCOL:
    Public message: <g><message>
    Private message: <p><name><to><message>
    List of users: <u>
    """

    def __init__(self, addr, port) -> None:

        self.addr = addr
        self.port = port
        self.login = False
        
        self.onlineClients = ["all"]

        self.name = "user"

        self.gui_done = False
        self.running = False

        # gui thread
        gui_thread = threading.Thread(target=self.gui)
        gui_thread.start()

        # receiving thread
        receive_message_thread = threading.Thread(target=self.receive)
        receive_message_thread.start()

    def getName(self):
        w = tkinter.Tk()
        w.withdraw()
        n = simpledialog.askstring("Insert name", "Please insert your name", parent=w)
        return n 

    def gui(self):
        self.win = tkinter.Tk()
        self.win.geometry("750x630")
        self.win.resizable(False,False)

        icon = PhotoImage(file='icon.png')
        self.win.iconphoto(True, icon)

        self.win.title("chat massenger")
        self.win.configure(bg="gray")

        # log button
        self.log_button = tkinter.Button(self.win, text="Log in", command=self.log)
        self.log_button.config(font=("Arial", 12))
        self.log_button.place(x = 40, y = 15)

        # name label
        self.name_label = tkinter.Label(self.win, text="Name: ", bg="gray")
        self.name_label.config(font=("Arial", 12))
        self.name_label.place(x = 180, y = 18)

        # name text area
        self.name_area = Entry(self.win, width=30)
        self.name_area.place(x = 280, y =  18)
        self.name_area.config(font=("Arial", 12))
        self.name_area.insert(0, self.name)
        self.name_area.config(state='disabled')
        
        # text area
        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.place(x = 40, y = 70)
        self.text_area.config(state='disabled')

        # message label
        self.msg_label = tkinter.Label(self.win, text="Message: ", bg="gray")
        self.msg_label.config(font=("Arial", 12))
        self.msg_label.place(x=350, y=465)

        # input area
        self.input_area = tkinter.Text(self.win, height=3)
        self.input_area.place(x=40, y=500)

        # to
        self.send_button = tkinter.Label(self.win, text="To: ", bg="gray")
        self.send_button.config(font=("Arial", 12))
        self.send_button.place(x=40, y=560)

        # to text area
        self.to = tkinter.StringVar()
        self.combobox = ttk.Combobox(self.win, width = 27, textvariable=self.to, state="readonly", postcommand=self.updateOnLineList)
        
        # Adding combobox drop down list
        self.combobox['values'] = self.onlineClients
        self.combobox.grid(column = 1, row = 5)
        self.combobox.place(x=80, y=565)
        self.combobox.current(0)

        # send button
        self.send_button = tkinter.Button(self.win, text="Send", command=self.send)
        self.send_button.config(font=("Arial", 12))
        self.send_button.place(x=350, y=560)

        # clear button
        self.clear_button = tkinter.Button(self.win, text="Clear", command=self.clear)
        self.clear_button.config(font=("Arial", 12))
        self.clear_button.place(x = 650, y = 18)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.exit)

        self.win.mainloop()

    def updateOnLineList(self):
        self.getOnlineUsers()
        time.sleep(0.2)
        self.combobox['values'] = self.onlineClients

    def log(self):
        if self.login == False:
            self.log_button["state"] = "disabled"
            self.name = self.getName()
            while self.name == None:
                self.name = self.getName()

            self.name_area.config(state='normal')
            self.name_area.delete(0, END)
            self.name_area.insert(0, self.name)
            self.name_area.config(state='disabled')

            self.log_button['text'] = 'Log out'
            self.log_button["state"] = "normal"
            self.sock = socket.socket()
            self.sock.connect((self.addr, self.port))
            self.sock.send(self.name.encode())

            self.running = True
            self.login = True
            print("logging in")
        else:
            self.sock.close()
            self.log_button['text'] = 'Log in'
            self.login = False
            print("logging out")

    def getOnlineUsers(self):
        if self.login == True:
            msg = "<u>".encode()
            self.sock.send(msg)

    def send(self):
        msg = ""
        if (self.to.get() == "all"):
            msg = ("<g><" + self.name + "><" + self.input_area.get('1.0', 'end') + ">")
        else:
            msg = ("<p><" + self.name + "><" + self.to.get() + "><" + self.input_area.get('1.0', 'end') + ">")

        self.sock.send(msg.encode())
        self.input_area.delete('1.0', 'end')

    def clear(self):
        self.text_area.config(state='normal')
        self.text_area.delete(1.0, END)
        self.text_area.config(state='disabled')

    def exit(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        
        while True:
            if self.running == False:
                continue

            try:
                recv = self.sock.recv(1024).decode()
                if("---online users names---\n" in recv):
                    l = recv.split("\n")[1].split(", ")
                    self.onlineClients.clear()
                    self.onlineClients.append("all")
                    for name in l:
                        self.onlineClients.append(name)
                    
                elif self.gui_done:
                    self.text_area.config(state='normal')
                    self.text_area.insert('end', recv)
                    self.text_area.yview('end')
                    self.text_area.config(state='disabled')

            except ConnectionAbortedError:
                break
            except:
                print("Error")
                self.sock.close()
                break
    
client = Client(SERVER_ADDRESS, PORT)

