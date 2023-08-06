import logging

from .constant import Constant

from messenger.helper import Utils
from messenger.helper.messaging import Message, Postback, Response
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

        logger.info("response: %s", response_text)
        post.send(Constant.send_api, response_text)

    def send_post_message(self, sender_psid, event):
        response = Response(Constant.messaging_type.response)
        response.set_recipient(sender_psid)
        response.set_text(event.text)

        post = Post(self.page_access_token)

        response_text = response.send_message()

        logger.info("response: %s", response_text)
        post.send(Constant.send_api, response_text)