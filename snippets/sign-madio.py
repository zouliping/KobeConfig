# -*- coding: utf-8 -*-
'''
Created on 2012-11-18

@author: liushuai
'''
import urllib, urllib2, cookielib, re

class LoginMadio:
    login_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4'}
    signin_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4','Referer':'http://www.madio.net','Origin':'http://www.madio.net'}
    username = ''
    password = ''
    formhash = ''
    cookie = None
    cookieFile = "./LoginMadio_Cookie.dat"
    
    def __init__(self, uname, pwd):
        self.username = uname
        self.password = pwd
        self.cookie = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        urllib2.install_opener(opener)
        
    def login(self):
        postdata = {'username':self.username, 'password':self.password, 'quickforward':'yes', 'handlekey':'ls'}
        postdata = urllib.urlencode(postdata)
        print self.username, 'is Logining...'
        req = urllib2.Request(url='http://www.madio.net/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1', data=postdata, headers=self.login_header)
        result = urllib2.urlopen(req).read()
        self.cookie.save(self.cookieFile)
        if '登录失败' in result or '密码错误' in result:
            print self.username,'login failed,please try later...'
        else :
            print self.username,'login successfully!'
        req_after_logining = urllib2.Request('http://www.madio.net/')
        html = urllib2.urlopen(req_after_logining).read()
        raw_str = str(re.search(r'<input type="hidden" name="formhash" value="\w+" />',html).group())
        raw_value = str(re.search(r'value="\w+"',raw_str).group())
        self.formhash = raw_value[7:len(raw_value) - 1]
        #print self.formhash
        
    def signin(self):
        postdata = {'formhash':self.formhash,'qdxq':'kx','qdmode':3,'todaysay':'','fastreply':1}
        postdata = urllib.urlencode(postdata)
        print self.username,'is signing...'
        req = urllib2.Request(url = 'http://www.madio.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&sign_as=1&inajax=1',data=postdata,headers=self.signin_header)
        result = urllib2.urlopen(req).read()
        self.cookie.save(self.cookieFile)
        if re.search(r'体力 \d+ 点',result) == None:
            print self.username,'sign in failed!Maybe you have signed in today or some other reasons...'
        else :
            raw_earn = str(re.search(r'体力 \d+ 点',result).group())
            earn = str(re.search(r'\d+',raw_earn).group())
            print self.username,'signed in successfully,you earn',earn,'points...'
    
if __name__ == '__main__':
    users = {"liushuaikobe1993@163.com":"XXX","zouliping007@163.com":"XXX","xxxpph@qq.com":"XXX"}
    for userName in users:
            user = LoginMadio(userName,users[userName])
            user.login()
            user.signin()
            print '-' * 60
    raw_input('Press Enter to terminate...')
