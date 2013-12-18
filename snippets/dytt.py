# -*- coding: utf-8 -*-
import re
import urllib

import smtplib
from email.mime.text import MIMEText

mail_config = {
    'from': 'gitradar@163.com',
    'to': 'liushuaikobe@gmail.com',
    'server': 'smtp.163.com',
    'username': 'gitradar',
    'pwd': 'footoo!@#$'
}

mail_list = ['liushuaikobe@gmail.com']

p1 = re.compile("""\[<a href="/html/gndy/dyzz/index\.html">最新电影下载</a>\]<a href='/html/gndy/dyzz/\d+/\d+\.html'>.+</a>""")
p2 = re.compile("""\[<a href="/html/gndy/index\.html">迅雷电影资源</a>\]<a href='/html/gndy/jddy/\d+/\d+\.html'>.+</a>""")


def sendmail(sbj, content, 
    fromwhom=mail_config['from'], towhom=mail_config['to'], 
    server=mail_config['server'], username=mail_config['username'], pwd=mail_config['pwd']):
    try:
        msg = msg.encode('utf-8')
    except Exception, e:
        pass
    msg = MIMEText(content, 'html')
    msg['Subject'] = sbj
    msg['From'] = fromwhom
    msg['To'] = towhom
    s = smtplib.SMTP(server)
    s.ehlo()
    s.starttls()
    s.login(username, pwd)
    s.sendmail(fromwhom, towhom, msg.as_string())

def foo():
	html = urllib.urlopen('http://www.dytt8.net/').read()
	html = html.decode('gb2312','ignore').encode('utf-8')

	movies = re.findall(p1, html)
	xls = re.findall(p2, html)

	movies = [movie.replace('/html', 'http://www.dytt8.net/html') for movie in movies]
	xls = [xl.replace('/html', 'http://www.dytt8.net/html') for xl in xls]

	#print movies	
	
	template = '<html><body><h3>最新电影</h3>{0}<br/><h3>迅雷资源</h3>{1}</body></html>'
	for m in mail_list:
		sendmail('movie', template.format('<br/>'.join(movies), '<br/>'.join(xls)), towhom=m)

foo()
