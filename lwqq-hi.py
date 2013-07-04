#-*- coding=utf-8 -*-

import os
import sys
curr_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(curr_path + os.sep + 'webpy')
import web
from webqq import WebQQ
from daemon import Daemon
from os import name as osname
import getpass
import time
import threading
from cgi import escape as htmlescape

LOG_PATH = curr_path + os.sep + 'qqbot_log'
ERR_PATH = curr_path + os.sep + 'qqbot_log_e'
TMPL_PATH = curr_path + os.sep + 'templates'

f_log = None

urls = (
    '/', 'log'
)

def reply_qq(sender_id, sender, msg):
    global f_log
    msg = msg.strip()
    f_log.write("<p>" + htmlescape(sender) + " : " + htmlescape(msg) + "</p>")
    f_log.flush()
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
        global f_log
        f_log = open(LOG_PATH, 'a+')
        t = threading.Thread(target = webserver)
        t.daemon = True
        t.start()
        while 1:
            try:
                self.qq.step()
            except KeyboardInterrupt:
                print "CTRL+C met, exit!"
                return
            except Exception as e:
                print "Error : ", e

def webserver():
    app = web.application(urls, globals())
    app.run()

class log:
    def GET(self):
        web.header('Content-type', "text/html; charset=utf-8")
        f = open(LOG_PATH)
        s = f.read()
        f.close()
        render = web.template.render(TMPL_PATH)
        return render.log(s)

if __name__ == "__main__":
    daemon = MyDaemon('/tmp/daemon-qqbot.pid', 
    stdout = ERR_PATH, 
    stderr = ERR_PATH)
    if osname == 'nt':
        daemon.qq_init()
        daemon.run()
    else:
        if len(sys.argv) >= 2:
            fa = sys.argv[1]
            sys.argv.remove(fa)
            if 'start' == fa:
                daemon.qq_init()
                daemon.start()
            elif 'stop' == fa:
                daemon.stop()
            elif 'restart' == fa:
                daemon.restart()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart" % sys.argv[0]
            sys.exit(2)
