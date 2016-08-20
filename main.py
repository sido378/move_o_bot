# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
from pymessenger.bot import Bot
from pprint import pprint

app = Flask(__name__)
DB_FILE = "data.json"
access_token = 'EAAPlE5lfeCwBALdFDfGaBLGzu9akZCcc4K5oAsMUVC2tCRUdVpLRr1PII4BoTtWPRbgf9LON9HcTB7G1GLBIafJr9Wz8t4d41Yx7tG21AZC9gRW4jMU49Jhwk14cSDDG4Qgq8l79F6LH0bSOkIAldSxu9RIjZB6mZCCPnokHsAZDZD'

bot = Bot(access_token)

with open('data.json') as data_file:
  user_db = json.load(data_file)

pprint(user_db)

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

