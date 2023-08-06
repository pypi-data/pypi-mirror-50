import logging

from .constant import Constant

from messenger.helper import Utils
from messenger.helper.messaging import Message, Postback, Response, QuickReply
from messenger.helper.http import Post

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger=logging.getLogger(__name__)

class Bot:
    def __init__(self, page_access_token, **kwargs):
        self.page_access_token = page_access_token

    def unpack_json(self, json):
        utils = Utils()
        chat_id, chat_time, sender_psid, event = utils.json_to_var(json)

        return chat_id, chat_time, sender_psid, event
        
    #merge with unpack_json
    def unpack_json2(self, json):
        utils = Utils()
        thread_type, tid, psid, signed_request = utils.json_to_var2(json)

        return thread_type, tid, psid, signed_request

    #merge with unpack_json
    def unpack_json3(self, json):
        utils = Utils()
        sender_psid, event = utils.json_to_var3(json)

        return sender_psid, event

    def send_post_attachment(self, sender_psid, event):
        response = Response(messaging_type = Constant.messaging_type.response)
        response.set_recipient(sender_psid)
        response.set_text(event.text)

        post = Post(self.page_access_token)

        response_text = response.construct_response()

        logger.info("response: %s", response_text)
        post.send(Constant.send_api, response_text)

    def send_post_attachment_button(self, sender_psid, template_type, text, button_type, button_url, button_title,
                                    webview_height_ratio):
        response = Response(attachment_type = 'template')
        response.set_recipient(sender_psid)
        response.set_template_type(template_type)
        response.set_text(text)
        response.set_button_type(button_type)
        response.set_button_url(button_url)
        response.set_button_title(button_title)
        response.set_webview_height_ratio(webview_height_ratio)

        post = Post(self.page_access_token)

        response_text = response.send_attachment_button()

        logger.info("response_text: %s", response_text)
        logger.info("response_post: %s", post.send(Constant.send_api, response_text))

    def send_post_message(self, sender_psid, text):
        response = Response(Constant.messaging_type.response)
        response.set_recipient(sender_psid)
        response.set_text(text)

        post = Post(self.page_access_token)

        response_text = response.send_message()

        logger.info("response: %s", response_text)
        post.send(Constant.send_api, response_text)

    def send_post_quick_reply(self, sender_psid, text, quick_reply):
        response = Response(Constant.messaging_type.response)
        response.set_recipient(sender_psid)        
        response.set_text(text)

        post = Post(self.page_access_token)

        response_text = response.send_quick_reply(quick_reply)

        logger.info("response: %s", response_text)
        post.send(Constant.send_api, response_text)

#quick_reply1 = QuickReply()
#quick_reply1.set_title('Menu')
#quick_reply1.set_payload('menu')
                    
#quick_reply2 = QuickReply()
#quick_reply2.set_title('Pay')
#quick_reply2.set_payload('pay')

#quick_reply3 = QuickReply()
#quick_reply3.set_title('Cash on Delivery')
#quick_reply3.set_payload('cod')

#quick_reply = [quick_reply1, quick_reply2, quick_reply3]

#acess_token='EAAHVJkggwLoBAKo3f5JxQWC7quZAzmo6JxvwFfLSnP13Fj69ZCNEpiXUed47HodJaT9SelWYeZC6aZADN1gVMh9xLZACll0DkHdE2CfjwCLVh22ZBACZBfLkH2v3AANHRpkGClfhKTDcEBXOeJkS8IBP5cHqV50bz5jS8PAmKBGyTaFlGZC9T5tD'    
#messenger_bot = Bot(acess_token)
#messenger_bot.send_post_quick_reply(987657890, 'Do you want to change order, confirm (pay), or confirm (cash on delivery)?', quick_reply)