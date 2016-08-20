# -*- coding: utf-8 -*-
import json, urllib
from flask import Flask, request, abort
import requests
from pymessenger.bot import Bot

app = Flask(__name__)

access_token = 'EAAQIAC6xy4cBAPWuGWTUZCta83wmaJwdV4ujK6MmUywZCTvjWiVP53GyjCOVfKA33DWDty3rfholokTU10tLKmcqcGTbUPvL5hmJvdtej5DnFqeSxJRadtBKbBN7ujJNLdPlwCP3vquZBjHVAs9SB0VdGqGvNpdT3gNCXK1lwZDZD'

bot = Bot(access_token)

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

                    if 'text' in messaging_event['message']:
                        message_text = messaging_event['message']['text']

                        bot.send_text_message(sender_id, message_text)

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
