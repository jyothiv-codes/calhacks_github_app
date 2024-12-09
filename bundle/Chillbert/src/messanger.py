from twilio.rest import Client
import os

class Messanger:
        
	def __init__(self):
		account_sid = os.environ['TWILIO_ACCOUNT_SID']
		auth_token = os.environ['TWILIO_AUTH_TOKEN']
		self.client = Client(account_sid, auth_token)

	def sendMessage(self, msg, recipient):
		if len(msg)>1500:
			msg = msg[:1500]
		self.client.messages.create(
		from_='whatsapp:+14155238886',
		body=msg,
		to=f'whatsapp:{recipient}'
		)
		# print("Message sent")
