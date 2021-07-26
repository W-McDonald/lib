import requests
import json
import configparser as cfg
import sys
sys.dont_write_bytecode = True


class TelegramBot():

    def __init__(self, configfile):
        self.config = self.__parse_config(configfile)
        self.name = config['name']
        self.api_token = config['api_token']
        self.base = "https://api.telegram.org/bot{}/".format(self.token)
        self.update_id = None
        self.message = None
        self.chat = None
        self.chat_id = None
        self.sender = None
        self.sender_name = None
        self.message_text = None
        self.command = None
        self.response = None

    def __parse_config(self, config):
        parser = cfg.ConfigParser()
        parsed_config = parser.read(config)
        return parsed_config

    def send_message(self, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, self.response)
        requests.get(url)

    def parse_message(self, data):
        self.update_id = data['update_id']
        if 'message' in data.keys():
            self.message = data['message']
            self.chat = data['message']['chat']
            self.chat_id = data['message']['chat']['id']
            self.sender = data['message']['from']
            self.sender_name = data['message']['from']['first_name']
            if 'text' in data['message'].keys():
                self.message_text = data['message']['text'].lower()
            if 'entities' in data['message'].keys():
                if data['message']['entities'][0]['type'] == 'bot_command':
                    self.command = self.message_text

    def respond(self):
        if self.response:
            self.send_message(self.chat_id)
        self.response = None

    def get_updates(self, offset=None):
        url = self.base + "getUpdates?timeout=50"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

