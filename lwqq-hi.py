#-*- coding=utf-8 -*-

from webqq import WebQQ
from os import name as osname
import getpass
import time

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

def main():
    user = raw_input('QQ:')
    pwd = getpass.getpass('Password: ')
    qq = WebQQ(user, pwd)
    qq.on_gotmsg = reply_qq
    qq.login()
    while 1:
        time.sleep(0.5)
        try:
            qq.step()
        except KeyboardInterrupt:
            print "CTRL+C met, exit!"
            return
        except Exception as e:
            print "Error : ", e

if __name__ == "__main__":
    main()
