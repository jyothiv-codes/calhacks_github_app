from src.fileprocessing import FileProcessing
from src.chatbot import ChatBot
from src.messanger import Messanger
import os

from dotenv import load_dotenv


load_dotenv()


class AnalyseChat:

    def __init__(self):
        self.fp = FileProcessing('logs/emotion_logs')
        self.m = Messanger()
        self.setup_complete=False

    def setup(self):


        print('Setting up Chat Analysis')
        output_file = self.fp.processFile()
        self.cb = ChatBot(output_file)

        summary = self.cb.summarize()
        links = self.cb.getlinks(summary)
        self.sendChatSummary(summary)
        self.sendHelpfulLinks(links)
        print('sent messages')
        # self.cb.ask_anything_continuous()

    def sendChatSummary(self, summary_message):
        msg = f'Your patient XYZ recently spoke to me. Here is the summary of our conversation. \n{summary_message}'
        self.m.sendMessage(msg, os.environ['TWILIO_RECIPIENT'])

    def sendHelpfulLinks(self, link_message):
        msg = f'I really enjoyed our converation today. Based on our chat, here are a few helpful links for you!\n{link_message}'
        self.m.sendMessage(msg, os.environ['TWILIO_RECIPIENT'])

    def askChatbot(self, question):
        resp = self.cb.ask_anything(question)
        # print(f'Response:{resp}')
        return resp

# ac = AnalyseChat()
# ac.setup()
# print(ac.askChatbot('How are the users emotions?'))