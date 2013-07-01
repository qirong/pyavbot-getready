#-*- coding=utf-8 -*-

import urllib2
import random
import cookielib
import json
import hashlib
import time

def time_stamp():
    return str(int(time.time()))

def hex_md5hash(s):
    return hashlib.md5(s).hexdigest().upper()

def hexchar2bin(uin):
    uin_final = ""
    uin = uin.split('\\x')
    for i in uin[1:]:
        uin_final += chr(int(i, 16))
    return uin_final

def md5_2(pwd, verifyCode1, verifyCode2):
    pwd_1 = hashlib.md5(pwd).digest()
    pwd_2 = hex_md5hash(pwd_1 + hexchar2bin(verifyCode2))
    pwd_final = hex_md5hash(pwd_2 + verifyCode1.upper())
    return pwd_final

QQ_API_BASE = 'http://s.web2.qq.com/api/'
QQ_REFERER = \
'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2'

class WebQQ:
    def __init__(self, user, pwd):
        self.cookies = cookielib.CookieJar()
        self.opener = urllib2.build_opener(
                urllib2.HTTPHandler(),
                urllib2.HTTPSHandler(),
                urllib2.HTTPCookieProcessor(self.cookies),
                )
        urllib2.install_opener(self.opener)
        self.user = user
        self.pwd = pwd
        self.clientid = str(random.randint(10000000, 99999999))
    
    def login(self):
        self.get_safe_code()
        self.login_get()
        self.login_post()

    def get_safe_code(self):
        url = \
        'https://ssl.ptlogin2.qq.com/check?uin=' + str(self.user) + \
        '&appid=1003903&js_ver=10017&js_type=0' \
        '&login_sig=0ihp3t5ghfoonssle-98x9hy4uaqm' \
        'pvu*8*odgl5vyerelcb8fk-y3ts6c3*7e8-&u1=' \
        'http%3A%2F%2Fweb2.qq.com%2Floginproxy.html' \
        '&r=0.8210972726810724'
        a = urllib2.urlopen(url).read().split("'")
        self.check = a[1]
        self.verifycode1 = a[3]
        self.verifycode2 = a[5]
        if self.check == "1":
            url = \
            'https://ssl.captcha.qq.com/getimage?&uin=' + \
            str(self.user) + '&aid=1002101&0.45644426648505' + \
            str(random.randint(10,99))
            req = urllib2.urlopen(url)
            fi = open("./image.jpg", "wb")
            while 1:
                c = req.read()
                if not c:
                    break
                else :
                    fi.write(c)
            fi.close()
            print "Please look at ./image.jpg .."
            self.verifycode1 = raw_input("Verifer : ")
    
    def login_get(self):
        login_url = 'https://ssl.ptlogin2.qq.com/login?u=' + \
        self.user + '&p=' + \
        str(md5_2(self.pwd, self.verifycode1, self.verifycode2)) + \
        '&verifycode=' + self.verifycode1 + \
        '&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=' \
        'http%3A%2F%2Fweb.qq.com%2Floginproxy.html%3Flogin2qq%3D1' \
        '%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&from_ui=' \
        '1&pttype=1&dumy=&fp=loginerroralert&action=2-14-32487&mi' \
        'bao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10015&login_sig' \
        '=0ihp3t5ghfoonssle-98x9hy4uaqmpvu*8*odgl5vyerelcb8fk-y3t' \
        's6c3*7e8-'
        req = urllib2.Request(login_url)
        req.add_header("Referer", 
        "https://ui.ptlogin2.qq.com/cgi-bin/login?" \
        "target=self&style=5&mibao_css=m_webqq&appid=1003903&" \
        "enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fwe" \
        "b.qq.com%2Floginproxy.html&f_url=loginerroralert&str" \
        "ong_login=1&login_state=10&t=" + time_stamp())
        req = urllib2.urlopen(req)
        req.read()
        for cookie in self.cookies:
            if cookie.name == 'ptwebqq':
                self.ptwebqq = cookie.value
        urllib2.urlopen(
        'http://web2.qq.com/web2/get_msg_tip?uin=&tp=1&id=0' \
        '&retype=1&rc=0&lv=3&t=' + time_stamp()).read()
    
    def login_post(self):
        url = 'http://d.web2.qq.com/channel/login2'
        r = {"status": "online", 
        "ptwebqq": self.ptwebqq, 
        "clientid": self.clientid, 
        "psessionid": None}
        data = 'r=' + urllib2.quote(json.dumps(r)) + \
        '&clientid=' + self.clientid + '&psessionid=null'
        self.result = json.load(self.smoothly_POST_open(url, data))
        self.psessionid = self.result['result']['psessionid']
        self.psessionid = \
        self.psessionid.decode("ascii").encode("utf-8")
        self.vfwebqq = self.result['result']['vfwebqq']
        self.vfwebqq = \
        self.vfwebqq.decode("ascii").encode("utf-8")
    
    def poll_msg(self):
        url = 'http://d.web2.qq.com/channel/poll2'
        r = {"clientid": self.clientid, 
        "psessionid": self.psessionid, 
        "key": 0, "ids": []}
        data = 'r=' + urllib2.quote(json.dumps(r)) + \
        '&clientid=' + self.clientid + \
        '&psessionid=' + self.psessionid
        return json.load(self.smoothly_POST_open(url, data))
    
    def send_msg(self, uin, msg):
        url = 'http://d.web2.qq.com/channel/send_buddy_msg2'
        self.smoothly_POST(url, self.build_msg_data(uin, msg))
    
    def send_group_msg(self, uin, msg):
        url = 'http://d.web2.qq.com/channel/send_qun_msg2'
        self.smoothly_POST(url, self.build_msg_data(uin, msg, True))
    
    def smoothly_POST(self, url, data):
        return self.smoothly_POST_open(url, data).read()
    
    def smoothly_POST_open(self, url, data):
        req = urllib2.Request(url, data)
        req.add_header('Referer', QQ_REFERER)
        return urllib2.urlopen(req)
    
    def smoothly_GET_open(self, url, data):
        req = urllib2.Request(url + '?' + data)
        req.add_header('Referer', QQ_REFERER)
        return urllib2.urlopen(req)
    
    def build_msg_data(self, uin, msg, in_group=False):
        font = {"name": "微软雅黑", 
        "size": 10, 
        "style": [0, 0, 0], 
        "color": "000000"}
        content = [msg, ["font", font]]
        uin_type = "to"
        if in_group:
            uin_type = "group_uin"
        r = {uin_type: uin, 
        "face" : 237, 
        "content": json.dumps(content), 
        "msg_id": 13190001, 
        "clientid": self.clientid, 
        "psessionid": self.psessionid}
        data = 'r=' + urllib2.quote(json.dumps(r)) + \
        '&clientid=' + self.clientid + \
        '&psessionid=' + self.psessionid
        return data
    
    def get_friend_info(self, uin):
        url = QQ_API_BASE + 'get_friend_info2'
        data = \
        'tuin=' + uin + '&verifysession=&code=&vfwebqq=' + \
        self.vfwebqq + '&t=' + time_stamp()
        return json.load(self.smoothly_GET_open(url, data))

    def get_nick(self, uin):
        inf = self.get_friend_info(uin)
        if inf.has_key("result"):
            if inf["result"].__class__ == {}.__class__:
                if inf["result"].has_key("nick"):
                    return inf["result"]["nick"].encode("utf-8")
        return uin
    
    def parse_message_json_part(self, it):
        if not (it.has_key("poll_type") and it.has_key("value")):
            return
        poll_type = it["poll_type"]
        value = it["value"]
        if not (poll_type in ("message", "group_message")):
            return
        uin = "%d" % value["from_uin"]
        msg = ""
        if value["content"][1].__class__ == u"".__class__:
            msg = value["content"][1].encode("utf-8")
        else:
            return
        nick = self.get_nick(uin)
        if value.has_key("group_code"):
            nick = self.get_group_member_nick(
            "%d" % value["group_code"], 
            "%d" % value["send_uin"])
        reply = self.on_gotmsg(uin, nick, msg)
        if (reply != "") and (reply.__class__ == "".__class__):
            if poll_type == "group_message":
                self.send_group_msg(uin, reply)
            self.send_msg(uin, reply)
    
    def parse_qq_json(self, a):
        if a.has_key("result"):
            result = a["result"]
        else:
            return
        if result.__class__ != [].__class__:
            return
        for it in result:
            self.parse_message_json_part(it)
    
    def get_group_member_info(self, gid, uin):
        url = QQ_API_BASE + 'get_group_info_ext2'
        data = 'gcode=' + gid + \
        '&vfwebqq=' + self.vfwebqq + \
        '&t=' + time_stamp()
        got = json.load(self.smoothly_GET_open(url, data))
        if not got.has_key("result"):
            return {}
        minfo = got["result"]["minfo"]
        for it in minfo:
            if ("%d" % it["uin"]) == uin:
                return it
        return {}
    
    def get_group_member_nick(self, gid, uin):
        inf = self.get_group_member_info(gid, uin)
        if inf.has_key("nick"):
            return inf["nick"].encode("utf-8")
        return uin
    
    def step(self):
        self.parse_qq_json(self.poll_msg())

