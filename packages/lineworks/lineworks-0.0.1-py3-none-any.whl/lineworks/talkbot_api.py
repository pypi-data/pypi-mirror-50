#  cording:utf-8

import json

from .server_api import ServerApi


class TalkBotApi(ServerApi):
    ''' Talkbot API class.

    Currently, the features that can be implemented are as follows:

    ・Create a private talk bot and a talk room with multiple users
    ・Send text messages from Talk Bot to users or talk rooms
    '''

    def __init__(self, api_id, private_key, server_api_consumer_key, server_id, bot_no, account_id="", room_id=""):
        ''' Constructor '''
        super().__init__(api_id, private_key, server_api_consumer_key, server_id)
        self.BOT_NO = bot_no
        self.ACCOUNT_ID = account_id
        self.ROOM_ID = room_id

    def create_room(self):
        ''' Create a new talk room with a private Bot.

        By line works specification, you must publish the Bot to all users before you can invite it to an existing talk room.
        Use this method to create a talk room that contains a private Bot.

        :return(str): Room Id of the created talk room.
        '''
        request_url = "https://apis.worksmobile.com/r/{}/message/v1/bot/{}/room".format(self.API_ID, self.BOT_NO)
        payload = {
            "accountIds": ["rei@re1yan"],
            "title": "Test Bot"
        }
        self.use_server_api(request_url=request_url, payload=payload)

    def send_message(self, content_dict):
        ''' The base method for sending messages.

        You can change the contents of the message by changing the argument (countent_dict).

        :param content_dict(dict): The content of the message.
        :return: If the call succeeds, it returns http 200 code.
        '''
        request_url = "https://apis.worksmobile.com/r/{}/message/v1/bot/{}/message/push".format(self.API_ID, self.BOT_NO)
        payload = {
            "botNo": str(self.BOT_NO),
        }

        # accountIdとroomIdはどちらか一方を指定
        if self.ACCOUNT_ID != "":
            payload.update({"accountId": str(self.ACCOUNT_ID)})
        elif self.ROOM_ID != "":
            payload.update({"roomId": str(self.ROOM_ID)})
        else:
            print("Please specify either ACCOUNT_ID or ROOM_ID.")
        payload.update(content_dict)
        json.loads(self.use_server_api(request_url=request_url, payload=payload))

    def send_text_message(self, send_text):
        ''' Send a text message.

        :param send_text(str): Messages sent to talkbot.

        :return: If the call succeeds, it returns http 200 code.
        '''
        content_dict = {
            "content": {
                "type": "text",
                "text": send_text
            }
        }
        self.send_message(content_dict=content_dict)