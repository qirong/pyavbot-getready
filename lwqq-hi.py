#-*- coding=utf-8 -*-

from webqq import WebQQ
from daemon import Daemon
from os import name as osname
import getpass
import time
import sys
import os

def reply_qq(sender_id, sender, msg):
    msg = msg.strip()
    if osname == 'nt':
        print sender.decode("utf-8").encode("gbk"), " : ", \
        msg.decode("utf-8").encode("gbk")
    else:
        print sender, " : ", msg
    if msg == "醒醒，醒醒":
        if sender != "":
            return sender + "，来啦来啦~"
        else:
            return "来啦来啦~"
    else:
        return ""

class MyDaemon(Daemon):
    def qq_init(self):
        user = raw_input('QQ:')
        pwd = getpass.getpass('Password: ')
        self.qq = WebQQ(user, pwd)
        self.qq.on_gotmsg = reply_qq
        self.qq.login()
    def run(self):
        while 1:
            try:
                self.qq.step()
            except KeyboardInterrupt:
                print "CTRL+C met, exit!"
                return
            except Exception as e:
                print "Error : ", e

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-qqbot.pid', stdout=(os.getcwd() + os.sep + 'qqbot_log'))
    if osname == 'nt':
        daemon.qq_init()
        daemon.run()
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.qq_init()
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)
