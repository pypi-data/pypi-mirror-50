class Response:

    def __init__(self, messaging_type = '', attachment_type = '', **kwargs):
        self.recipient_psid = ''

        self.messaging_type = messaging_type
        self.text = ''
        
        self.attachment_type = attachment_type
        self.payload_url = ''
        self.payload_reusable = True

        self.template_type = ''
        self.button_type = ''
        self.button_url = ''
        self.button_title = ''
        self.webview_height_ratio = ''
        self.messenger_extensions = False
        
        return super().__init__(**kwargs)

    def set_recipient(self, recipient_psid):
        self.recipient_psid = recipient_psid

    def set_text(self, text):
        self.text = text
    def set_messaging_type(self, messaging_type):
        self.messaging_type = messaging_type
        
    def set_attachment_type(self, attachment_type):
        self.attachment_type = attachment_type
    def set_payload_url(self, payload_url):
        self.payload_url = payload_url
    def set_payload_reusable(self, payload_reusable):
        self.payload_reusable = payload_reusable

    def set_template_type(self, template_type):
        self.template_type = template_type
    def set_button_type(self, button_type):
        self.button_type = button_type
    def set_button_url(self, button_url):
        self.button_url = button_url
    def set_button_title(self, button_title):
        self.button_title = button_title
    def set_webview_height_ratio(self, webview_height_ratio):
        self.webview_height_ratio = webview_height_ratio
        
    def send_attachment_button(self):
        response = {}

        if not self.recipient_psid:
            print('recipient cannot be blank')
            return ''

        response['recipient'] = {'id' : self.recipient_psid}
        response['message'] = {}
        response['message']['attachment'] = {}
        response['message']['attachment']['type'] = self.attachment_type
        response['message']['attachment']['payload'] = {}

        response['message']['attachment']['payload']['template_type'] = self.template_type
        response['message']['attachment']['payload']['text'] = self.text
        
        response['message']['attachment']['payload']['buttons'] = []
        response['message']['attachment']['payload']['buttons'].append({})
        response['message']['attachment']['payload']['buttons'][0]['type'] = self.button_type
        response['message']['attachment']['payload']['buttons'][0]['url'] = self.button_url
        response['message']['attachment']['payload']['buttons'][0]['title'] = self.button_title
        response['message']['attachment']['payload']['buttons'][0]['webview_height_ratio'] = self.webview_height_ratio
        response['message']['attachment']['payload']['buttons'][0]['messenger_extensions'] = self.messenger_extensions

        return response
    def send_attachment_file(self):
        response = {}

        if not self.recipient_psid:
            print('recipient cannot be blank')
            return ''

        response['recipient'] = {'id' : self.recipient_psid}
        response['message'] = {}
        response['message']['attachment'] = {}
        response['message']['attachment']['type'] = self.attachment_type
        response['message']['attachment']['payload'] = {}
        
        if not self.payload_url:
            print('payload_url cannot be blank')
            return ''

        response['message']['attachment']['payload']['url'] = self.payload_url
        response['message']['attachment']['payload']['is_reusable'] = self.payload_reusable

        response['message']['attachment'] = {'text' : self.text}

        return response

    def send_message(self):
        response = {}

        response['messaging_type'] = self.messaging_type
        
        if not self.recipient_psid:
            print('recipient cannot be blank')
            return ''

        response['recipient'] = {'id' : self.recipient_psid}

        if self.text:
            response['message'] = {'text' : self.text}

        return response