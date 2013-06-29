#-*- coding=utf-8 -*-

import urllib2
import random
import cookielib
import json
import hashlib

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
        self.getSafeCode()
        self.loginGet()
        self.loginPost()

    def getSafeCode(self):
        url = 'https://ssl.ptlogin2.qq.com/check?uin=' + str(self.user) + '&appid=1003903&js_ver=10017&js_type=0&login_sig=0ihp3t5ghfoonssle-98x9hy4uaqmpvu*8*odgl5vyerelcb8fk-y3ts6c3*7e8-&u1=http%3A%2F%2Fweb2.qq.com%2Floginproxy.html&r=0.8210972726810724'
        req = urllib2.Request(url)
        req  = urllib2.urlopen(req)
        a = req.read().split("'")
        self.check = a[1]
        self.verifycode1 = a[3]
        self.verifycode2 = a[5]
        if self.check == "1":
            url = 'https://ssl.captcha.qq.com/getimage?&uin='+str(self.user)+'&aid=1002101&0.45644426648505' + str(random.randint(10,99))
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

    def loginGet(self):
        login_url = 'https://ssl.ptlogin2.qq.com/login?u='+self.user +'&p=' + str(md5_2(self.pwd, self.verifycode1, self.verifycode2)) + '&verifycode=' + self.verifycode1 + '&webqq_type=10&remember_uin=1&login2qq=1&aid=1003903&u1=http%3A%2F%2Fweb.qq.com%2Floginproxy.html%3Flogin2qq%3D1%26webqq_type%3D10&h=1&ptredirect=0&ptlang=2052&from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=2-14-32487&mibao_css=m_webqq&t=1&g=1&js_type=0&js_ver=10015&login_sig=0ihp3t5ghfoonssle-98x9hy4uaqmpvu*8*odgl5vyerelcb8fk-y3ts6c3*7e8-'
        req = urllib2.Request(login_url)
        req.add_header("Referer", "https://ui.ptlogin2.qq.com/cgi-bin/login?target=self&style=5&mibao_css=m_webqq&appid=1003903&enable_qlogin=0&no_verifyimg=1&s_url=http%3A%2F%2Fweb.qq.com%2Floginproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20121029001")
        req = urllib2.urlopen(req)
        req.read()
        for cookie in self.cookies:
            if cookie.name == 'ptwebqq':
                self.ptwebqq = cookie.value
        urllib2.urlopen('http://web2.qq.com/web2/get_msg_tip?uin=&tp=1&id=0&retype=1&rc=0&lv=3&t=1358252543124').read()

    def loginPost(self):
        url = 'http://d.web2.qq.com/channel/login2'
        data = 'r=%7B%22status%22%3A%22online%22%2C%22ptwebqq%22%3A%22' + self.ptwebqq + '%22%2C%22passwd_sig%22%3A%22%22%2C%22clientid%22%3A%22'+self.clientid+'%22%2C%22psessionid%22%3Anull%7D&clientid='+self.clientid+'&psessionid=null'
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2')
        req = urllib2.urlopen(req)
        self.result = json.load(req)
        self.result['result']['vfwebqq']
        self.result['result']['psessionid']

    def pollMsg(self):
        url = 'http://d.web2.qq.com/channel/poll2'
        data ='r=%7B%22clientid%22%3A%22' + self.clientid + '%22%2C%22psessionid%22%3A%22' + self.result['result']['psessionid']+'%22%2C%22key%22%3A0%2C%22ids%22%3A%5B%5D%7D&clientid=' + self.clientid + '&psessionid=' + self.result['result']['psessionid']
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=3')
        result = json.load(urllib2.urlopen(req))
        return result

    def sendMsg(self, uin, msg):
        url = 'http://d.web2.qq.com/channel/send_buddy_msg2'
        data = 'r=%7B%22to%22%3A'+uin+'%2C%22face%22%3A237%2C%22content'+urllib2.quote(r'":"[\"'+msg+r'\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","')+'msg_id%22%3A13190001%2C%22clientid%22%3A%22'+self.clientid+'%22%2C%22psessionid%22%3A%22'+self.result['result']['psessionid']+'%22%7D&clientid='+self.clientid+'&psessionid='+self.result['result']['psessionid']
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2')
        urllib2.urlopen(req).read()

    def sendQunMsg(self, uin, msg):
        url = 'http://d.web2.qq.com/channel/send_qun_msg2'
        data = 'r=%7B%22group_uin%22%3A'+uin+'%2C%22face%22%3A237%2C%22content'+urllib2.quote(r'":"[\"'+msg+r'\",[\"font\",{\"name\":\"宋体\",\"size\":\"10\",\"style\":[0,0,0],\"color\":\"000000\"}]]","')+'msg_id%22%3A13190001%2C%22clientid%22%3A%22'+self.clientid+'%22%2C%22psessionid%22%3A%22'+self.result['result']['psessionid']+'%22%7D&clientid='+self.clientid+'&psessionid='+self.result['result']['psessionid']
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://d.web2.qq.com/proxy.html?v=20110331002&callback=1&id=2')
        urllib2.urlopen(req).read()

"""
    def getGroupList(self):
        url = 'http://s.web2.qq.com/api/get_group_name_list_mask2'
        data = 'r=%7B%22vfwebqq%22%3A%22'+self.result['result']['vfwebqq'] +'%22%7D'
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=1')
        req = urllib2.urlopen(req)
        self.group = json.load(req)

    def getFriend(self):
        url = 'http://s.web2.qq.com/api/get_user_friends2'
        data = 'r=%7B%22vfwebqq%22%3A%22'+self.result['result']['vfwebqq'] +'%22%7D'
        req = urllib2.Request(url, data)
        req.add_header('Referer', 'http://s.web2.qq.com/proxy.html?v=20110412001&callback=1&id=1')
        req = urllib2.urlopen(req)
        self.friend = json.load(req)
        return self.friend
"""
