# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
from pymessenger.bot import Bot
from pprint import pprint

app = Flask(__name__)

access_token = 'EAAQIAC6xy4cBAPWuGWTUZCta83wmaJwdV4ujK6MmUywZCTvjWiVP53GyjCOVfKA33DWDty3rfholokTU10tLKmcqcGTbUPvL5hmJvdtej5DnFqeSxJRadtBKbBN7ujJNLdPlwCP3vquZBjHVAs9SB0VdGqGvNpdT3gNCXK1lwZDZD'
DB_FILE = "data.json"


bot = Bot(access_token)

with open('data.json') as data_file:
  user_db = json.load(data_file)

@app.route("/", methods=["GET"])
def root():
    return "Hello World!"


# webhook for facebook to initialize the bot
@app.route('/webhook', methods=['GET'])
def get_webhook():

    if not 'hub.verify_token' in request.args or not 'hub.challenge' in request.args:
        abort(400)

    return request.args.get('hub.challenge')


@app.route('/webhook', methods=['POST'])
def post_webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data['entry']:
            for messaging_event in entry['messaging']:

                if "message" in messaging_event:

                    sender_id = messaging_event['sender']['id']

                    if sender_id not in user_db:
                      user_db[sender_id] = {}
                      get_username(sender_id)
                      save_db()

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']
                        bot.send_text_message(sender_id, message_text)

                elif "postback" in messaging_event:
                    received_postback(messaging_event)
    return "ok", 200


def get_url(url):
    result = request.get(url)
    return json.loads(result.content)


def do_rules(recipient_id, message_text):
    rules = {
        "Hello": "World",
        "Foo": "Bar"
    }

    if message_text in rules:
        bot.send_text_message(recipient_id, message_text)
    else:
        bot.send_text_message(recipient_id, "You have to write something I understand ;)")


def received_postback(event):
    sender_id = event['sender']['id']
    payload = event['postback']['payload']
    if 'GETTING_STARTED' in payload:
        bot.send_text_message(sender_id, "Hi! My name is Hermes. Are you ready to get quizzed on history? Which topic do you want questions on?")
        # send_introduction


def save_db():
  with open('data.json', 'w') as data_file:
    json.dump(user_db, data_file)

def get_username(sender_id):
    url = "https://graph.facebook.com/v2.6/"+ sender_id +"?access_token="+ access_token
    result = requests.get(url)
    result = json.loads(result.text)
    user_db[sender_id]["name"]=result['first_name']
    save_db()
