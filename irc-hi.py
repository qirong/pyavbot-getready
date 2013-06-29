#-*- coding:utf-8 -*-

import socket

def login_irc_freenode(nick):
    s = socket.create_connection(("irc.freenode.net", 6666))
    s.send("NICK " + nick + "\r\n")
    s.send("USER " + nick + " 0 * : " + nick + "\r\n")
    return s

def join_chatroom(s, chatroom):
    s.send("JOIN #" + chatroom + "\r\n")

def send_message(s, chatroom, msg):
    s.send("PRIVMSG #" + chatroom + " :" + msg + "\r\n")

channel = "test_bot_coleman"
socket_irc = login_irc_freenode("rosemary")
join_chatroom(socket_irc, channel)
while 1:
    re = socket_irc.recv(0xffffff)
    for line in re.split("\r\n"):
        if len(line) > 0:
            if line[0] == ':':
                if ("PRIVMSG #" + channel) in line:
                    name = line.split("!")[0][1:]
                    send_message(socket_irc, channel, 
                        name + "说得对!")

