"""
    Much like uwsgi server, your application code that is handling
    the protocol events run inside the server process itself.
    It means that the ChatConsumer code runs inside the websocket code,
    that allows it to receive events.
    Each socket or connection to your overall application is handled by
    an application instance. They get called and can send data back to the
    client directly.
    However as you build more complex appliction systems, you start needing
    to communicate between different application instances, for example if you
    are building a chatroom, when one application instance (i-e one user) receives
    an incoming message, it needs to distribute it out to any other instances that
    represents people in the chatroom.
    You can do this by putting the message in the database and then continuously
    pulling data from the database to check for new messages. This is very difficult
    to handle. Channel introduces the idea of channel layer, a low level abstraction
    around a set of transports that allow you to send information between different
    processes. Each application instance has a unique channel name, and can join groups
    allowing both point-to-point and broadcast messaging.
"""

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = 'chat_%s' % self.id
        # join room group
        # ChatConsumer is a synchronous websocket consumer
        # but group_add() method of the channel layer is
        # asynchronous, therefore to communicate between
        # sync to async we use a wrapper async_to_sync
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        # accept connection
        self.accept()

    def disconnect(self, close_code):
        pass

    # receive message from Websocket
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # send message to websocket
        self.send(text_data=json.dumps({'message': message}))
