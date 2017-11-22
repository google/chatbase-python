# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Define the attributes on facebook user messages."""

import json, requests
from .base_message import Message
from .facebook_chatbase_fields import *


class FacebookUserMessage(Message):
    """FacebookUserMessage represents a message
    garnered from a user via facebook.
    """

    def __init__(self, api_key="", intent="", version="", message=""):
        super(FacebookUserMessage, self).__init__(api_key=api_key,
                                                  intent=intent,
                                                  version=version,
                                                  message=message)
        self.sender = FacebookID()
        self.recipient = FacebookID()
        self.fb_message = FacebookUserMessageContent()
        self.timestamp = Message.get_current_timestamp()
        self.chatbase_fields = ChatbaseFields()

    def set_recipient_id(self, rec_id):
        """Set the recipient id."""
        self.recipient.id = rec_id

    def set_sender_id(self, snd_id):
        """Set the sender id."""
        self.sender.id = snd_id

    def set_message_id(self, msg_id):
        """Set the message id."""
        self.fb_message.mid = msg_id

    def set_chatbase_fields(self):
        """Extract chatbase fields from instance and format for transmission."""
        self.chatbase_fields.intent = self.intent
        self.chatbase_fields.version = self.version
        self.chatbase_fields.not_handled = self.not_handled
        self.chatbase_fields.feedback = self.feedback
        self.fb_message.text = self.message

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        self.set_chatbase_fields()
        return json.dumps({
            'sender': self.sender,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
            'message': self.fb_message,
            'chatbase_fields': self.chatbase_fields
        }, default=lambda i: i.__dict__)

    def to_set_format(self):
        """Return a dictionary version of the message for a set"""
        self.set_chatbase_fields()
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
            'message': self.fb_message,
            'chatbase_fields': self.chatbase_fields
        }

    def send(self):
        """Send the message to the Chatbase API."""
        url = ("https://chatbase.com/api/facebook/send_message?api_key=%s" %
               self.api_key)
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())

class FacebookUserMessageSet(object):
    """Message Set.
    Add messages to a set and send to the Batch API.
    """

    def __init__(self,
                 api_key="",
                 version=""):
        self.api_key = api_key
        self.version = version
        self.messages = []

    def new_message(self, intent="", message=""):
        """Add a message to the internal messages list and return it"""
        self.messages.append(FacebookUserMessage(api_key=self.api_key,
                                                 version=self.version,
                                                 intent=intent,
                                                 message=message))
        return self.messages[-1]

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        msgs = [msg.to_set_format() for msg in self.messages]
        return json.dumps({"messages": msgs}, default=lambda i: i.__dict__)

    def send(self):
        """Send the message set to the Chatbase API"""
        url = ("https://chatbase.com/api/facebook/message_received_batch?api_key=%s"
               % self.api_key)
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())
