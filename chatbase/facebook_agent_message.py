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

"""Define the attributes on facebook agent messages."""

import json
import requests
from base_message import Message
from facebook_chatbase_fields import *


class FacebookAgentMessageRequestBody(object):
    """Request body for facebook agent message."""

    def __init__(self):
        self.recipient = FacebookID()
        self.message = FacebookUserMessageContent()
        self.timestamp = Message.get_current_timestamp()


class FacebookAgentMessageResponseBody(object):
    """Request body for facebook agent message."""

    def __init__(self):
        self.recipient_id = ''
        self.message_id = ''


class FacebookAgentMessage(Message):
    """FacebookAgentMessage represents a message
    garnered from an agent via facebook.
    """

    def __init__(self, api_key="", intent="", version="", message=""):
        super(FacebookAgentMessage, self).__init__(api_key=api_key,
                                                   intent=intent,
                                                   version=version,
                                                   message=message)
        self.request_body = FacebookAgentMessageRequestBody()
        self.response_body = FacebookAgentMessageResponseBody()
        self.chatbase_fields = ChatbaseFields()

    def set_recipient_id(self, rec_id):
        """Set the recipient id."""
        self.response_body.recipient_id = rec_id
        self.request_body.recipient.id = rec_id

    def set_message_id(self, msg_id):
        """Set the message id."""
        self.response_body.message_id = msg_id
        self.request_body.message.mid = msg_id

    def set_chatbase_fields(self):
        """Extract chatbase fields from instance and format for transmission."""
        self.chatbase_fields.intent = self.intent
        self.chatbase_fields.version = self.version
        self.chatbase_fields.not_handled = self.not_handled
        self.chatbase_fields.feedback = self.feedback
        self.request_body.message.text = self.message

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        self.set_chatbase_fields()
        return json.dumps({
            'request_body': self.request_body,
            'response_body': self.response_body,
            'chatbase_fields': self.chatbase_fields
        }, default=lambda i: i.__dict__)

    def send(self):
        """Send the message to the Chatbase API."""
        url = ("https://chatbase.com/api/facebook/message_received?api_key=%s" %
               self.api_key)
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())


class FacebookAgentMessageSet(object):
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
        self.messages.append(FacebookAgentMessage(api_key=self.api_key,
                                                  version=self.version,
                                                  intent=intent,
                                                  message=message))
        return self.messages[-1]

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        [(lambda m: m.set_chatbase_fields())(m) for m in self.messages]
        return json.dumps({'messages': self.messages},
                          default=lambda i: i.__dict__)

    def send(self):
        """Send the message set to the Chatbase API"""
        url = ("https://chatbase.com/api/facebook/send_message_batch?api_key=%s"
               % self.api_key)
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())
