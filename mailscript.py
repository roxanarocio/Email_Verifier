
import re
import dns.resolver
import smtplib
from dns.exception import DNSException
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', metavar='in-file', type=argparse.FileType('rt'))
arguments = parser.parse_args()

for arg in arguments.i:
	print('Verifying the email address :' + arg)
	email = arg.strip()
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

	if match == None:
		print('Syntax Error')
	else:
		splitAddress = email.split('@')
		domain = str(splitAddress[1])
		print('Domain to check:', domain)

		try:
			mxRecords = dns.resolver.query(domain, 'MX')

			for mx in mxRecords:
       				print(mx.to_text(), 'mxRecord')

			mxRecord = mxRecords[0].exchange

			server = smtplib.SMTP()

			response = server.connect(str(mxRecord))

			response = server.ehlo("hola")
			print(response)


			faikfrom = "faikmail@faikdomain.com"
			response = server.mail(faikfrom)
			print(response)
			r_code, r_message = server.rcpt(email)
			print(r_code, r_message)
			server.quit() 

			if r_code == 550:
	        		print("THIS IS NOT A VALID EMAIL ADDRESS!\n")
			else: 
	        		print("THIS IS A VALID EMAIL ADDRESS\n")

		except :
			print('DOMAIN NOT VALID\n')
