from telebot import types as teletypes
from datetime import datetime


class LoggedMessage:
    def __init__(self, text, user_id, from_user, **kwargs):
        self.text = text
        self.user_id = user_id
        self.from_user = from_user
        self.timestamp = str(datetime.utcnow())
        self.kwargs = kwargs

    def save_to_mongo(self, collection):
        collection.insert_one(self.to_dict())

    def to_dict(self):
        result = {
            'text': self.text,
            'user_id': self.user_id,
            'from_user': self.from_user,
            'timestamp': self.timestamp
        }
        for k, v in self.kwargs.items():
            if k not in result:
                result[k] = v
        return result

    @classmethod
    def from_telegram(cls, message: teletypes.Message, **kwargs):
        reply_to_id = None
        if message.reply_to_message is not None:
            reply_to_id = message.reply_to_message.message_id
        return cls(
            text=message.text,
            user_id=message.chat.id,
            message_id=message.message_id,
            from_user=not message.from_user.is_bot,
            username=message.chat.username,
            reply_to_id=reply_to_id,
            source='telegram',
            **kwargs
        )

    @classmethod
    def from_alice(cls, message, **kwargs):
        return cls(
            text=message['response']['text'] if 'response' in message else message['request']['original_utterance'],
            user_id=message['session']['user_id'],
            from_user='response' not in message,
            data=message,
            source='alice',
            **kwargs
        )
