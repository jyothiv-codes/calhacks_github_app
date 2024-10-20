from twilio.rest import Client
from chatbot import ChatBot
import os
from dotenv import load_dotenv


load_dotenv()


class Messages:
        
	def __init__(self):
		account_sid = os.environ['TWILIO_ACCOUNT_SID']
		auth_token = os.environ['TWILIO_AUTH_TOKEN']
		self.client = Client(account_sid, auth_token)

	def sendMessage(self, msg, recipient):
		self.client.messages.create(
		from_='whatsapp:+14155238886',
		body=msg,
		to=f'whatsapp:{recipient}'
		)
		print("Message sent")

	def sendChatSummary(self):
		cb = ChatBot()
		msg = f'Your patient XYZ recently spoke to me. Here is the summary of our conversation. \n{cb.summarize()}'
		self.sendMessage(msg, os.environ['TWILIO_RECIPIENT'])


	def sendHelpfulLinks(self):
		cb = ChatBot()
		msg = f'I really enjoyed our converation today. Based on our chat, here are a few helpful links for you!\n{cb.getlinks()}'
		self.sendMessage(msg, os.environ['TWILIO_RECIPIENT'])


m = Messages()
m.sendHelpfulLinks()
