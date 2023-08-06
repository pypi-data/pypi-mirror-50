#import messaging.message as m
#import messaging.postback as p
from messenger.helper.messaging import Message, Postback

class Utils:
    def json_to_var(self, json):
        obj = json['object']
        chat_id = chat_time = sender_psid = event = ''
        message = Message()
        postback = Postback()

        #there may be multiple if batched: developers.facebook.com/docs/messenger-platform/getting-started/quick-start
        #not handled, no batch processing yet
        #for entry in json['entry']:
        entry = json['entry'][0]
            
        chat_id = entry['id']
        chat_time = entry['time']

        webhook_event = entry['messaging'][0]
        sender_psid = webhook_event['sender']['id']
        #recipient_psid not handled

        if webhook_event.get('message'):
            message.json_to_message(webhook_event['message'])
            event = message
        elif webhook_event.get('postback'):
            postback.json_to_message(webhook_event['postback'])
            event = postback

        return chat_id, chat_time, sender_psid, event