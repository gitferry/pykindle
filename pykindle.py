#!/usr/bin/env python
# coding=utf-8


'''
a simple program that can write a email to kindle and convert the pdf to kindle file
'''


import smtplib, sys, os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

class MyEmail(object):
	"""my email class"""
	def __init__(self, from_address, to_address, subject):
		self.msg = MIMEMultipart()
		self.msg['From'] = from_address
		self.msg['To'] = to_address
		self.msg['Date'] = formatdate(localtime=True)
		self.msg['Subject'] = subject

		print "Create email from '%s' to '%s', subject is '%s'" % (self.msg['From'], self.msg['To'], self.msg['Subject'])

	def wrap_attachment(self, files_list):
		self.msg.attach(MIMEText(""))

		for f in files_list:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( open(f,"rb").read() )
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
			self.msg.attach(part)


	def send_email(self, server, username, password):
		try:
			print '正在连接邮件服务器...'
			server = smtplib.SMTP(server, timeout=30)
			server.ehlo()
			server.starttls()
			server.login(username, password)
			print '正在发送...'
			server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
			server.close()
			print '发送成功'
		except Exception, e:
			print str(e)


def configure():
    from_address = raw_input("What's your address?\n")
    to_address = raw_input("Where to?\n")
    subject = raw_input("what's the subject?\n")
    username = raw_input("What's your user name?\n")
    password = raw_input("Please input your password:\n")

    context = "\n".join([from_address, to_address, subject, username, password])

    f = open('config', 'w')

    f.write(context)
    f.close()


def load_config():
    try:
        f = open('config', 'r')
        contex = f.readlines()
        from_address = contex[0]
        to_address = contex[1]
        subject = contex[2]
        username = contex[3]
        password = contex[4]

        f.close()
    except:
        print "Please configure first."
        sys.exit(1)

    return  from_address, to_address, subject, username, password


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('USAGE: %s <stem>\n' % sys.argv[0])
        sys.exit(1)

    if sys.argv[1] == '-c':
        configure()
    else:
        print 'send ', sys.argv[1]

        from_address, to_address, subject, username, password = load_config()

        newEmail = MyEmail(from_address=from_address, to_address=to_address, subject=subject)

        server = "smtp.gmail.com:587"

        files = [sys.argv[1]]
        newEmail.wrap_attachment(files)
        newEmail.send_email(server, username, password)
