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

		# print "Create email from %s to %s, subject is" % (from_address, to_address, subject)

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


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('USAGE: %s <stem>\n' % sys.argv[0])
        sys.exit(1)
    print 'send ', sys.argv[1]

    from_address = 'greferry@gmail.com'
    to_address = 'gaigai508@kindle.cn'
    subject = 'convert'

    newEmail = MyEmail(from_address=from_address, to_address=to_address, subject=subject)

    server = "smtp.gmail.com:587"
    username = "greferry"
    password = "gaigaiforgoogle"

    files = [sys.argv[1]]
    newEmail.wrap_attachment(files)
    newEmail.send_email(server, username, password)