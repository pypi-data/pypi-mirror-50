class Constant:
    default_api_version = 2.6
    send_api = 'https://graph.facebook.com/v%s/me/messages'%default_api_version
    
    class attachment_type:
        audio = 'AUDIO'
        video = 'VIDEO'
        image = 'IMAGE'
        file = 'FILE'
        template = 'TEMPLATE'

    class messaging_type:
        response = 'RESPONSE'
        update = 'UPDATE'
        message_tag = 'MESSAGE_TAG'

