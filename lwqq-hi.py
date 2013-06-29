#-*- coding=utf-8 -*-

from webqq import WebQQ
from os import name as osname
import getpass
import time


def get_reply(msg):
    msg = msg.strip()
    if msg == "醒醒，醒醒":
        return "来啦来啦~"
    return ""

def parse_qq_json(qq, a):
    if a.has_key("result"):
        if a["result"].__class__ == [].__class__:
            for it in a["result"]:
                if (it["poll_type"] == "message") or \
                (it["poll_type"] == "group_message"):
                    uin = "%d" % it["value"]["from_uin"]
                    msg = ""
                    if it["value"]["content"][1].__class__ == u"".__class__:
                        msg = it["value"]["content"][1].encode("utf-8")
                    reply = get_reply(msg)
                    if reply != "":
                        if it["poll_type"] == "group_message":
                            qq.sendQunMsg(
                                "%d" % it["value"]["from_uin"], reply)
                        qq.sendMsg(
                            "%d" % it["value"]["from_uin"], reply)
                    if osname == 'nt':
                        print uin, ":", msg.decode("utf-8").encode("gbk")
                    else:
                        print uin, ":", msg

def main():
    user = raw_input('QQ:')
    pwd = getpass.getpass('Password: ')
    qq = WebQQ(user, pwd)
    qq.login()
    while 1:
        time.sleep(0.5)
        try:
            parse_qq_json(qq, qq.pollMsg())
        except KeyboardInterrupt:
            print "CTRL+C met, exit!"
            return
        except Exception as e:
            print "Error : ", e

if __name__ == "__main__":
    main()
