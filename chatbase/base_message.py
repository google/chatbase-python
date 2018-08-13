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

"""Define the core attributes/methods on a Message instance."""
import json
import requests
import time


class InvalidMessageTypeError(Exception):
    """Error raised when attribute values are set on a
    Message instance which is not compatible with the
    the msg_type attribute.
    """

    def __init___(self, val):
        self.value = val

    def __str__(self):
        return repr(self.value)


class MessageTypes(object):
    """Defines message types."""
    USER = "user"
    AGENT = "agent"


class Message(object):
    """Base Message.
    Define attributes present on all variants of the Message Class.
    """

    def __init__(self,
                 api_key="",
                 platform="",
                 message="",
                 intent="",
                 version="",
                 user_id="",
                 session_id="",
                 type=None,
                 not_handled=False,
                 time_stamp=None):
        self.api_key = api_key
        self.platform = platform
        self.message = message
        self.intent = intent
        self.version = version
        self.user_id = user_id
        self.session_id = session_id
        self.not_handled = not_handled
        self.feedback = False
        self.time_stamp = time_stamp or Message.get_current_timestamp()
        self.type = type or MessageTypes.USER

    @staticmethod
    def get_current_timestamp():
        """Returns the current epoch with MS precision."""
        return int(round(time.time() * 1e3))

    @staticmethod
    def get_content_type():
        """Returns the content-type for requesting against the Chatbase API"""
        return {'Content-type': 'application/json', 'Accept': 'text/plain'}

    def set_as_type_user(self):
        """Set the message as type user."""
        self.type = MessageTypes.USER

    def set_as_type_agent(self):
        """Set the message as type agent."""
        self.type = MessageTypes.AGENT

    def set_as_not_handled(self):
        """Set the message's not_handled attribute to True.
        Will throw if the message is of type Agent. Only user-type
        Messages can have the not_handled attribute as True.
        """
        if self.type == MessageTypes.AGENT:
            raise InvalidMessageTypeError(
                'Cannot set not_handled as True when msg is of type Agent')
        self.not_handled = True

    def set_as_handled(self):
        """Set the message's not_handled attribute to False."""
        self.not_handled = False

    def set_as_feedback(self):
        """Set the message's feedback attribute to True.
        Will throw if the message is of type Agent. Only user-type
        Messages can have the feedback attribute as True.
        """
        if self.type == MessageTypes.AGENT:
            raise InvalidMessageTypeError(
                'Cannot set feedback as True when msg is of type Agent')
        self.feedback = True

    def set_as_not_feedback(self):
        """Set the message's feeback attribute to False."""
        self.feedback = False

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        return json.dumps(self, default=lambda i: i.__dict__)

    def send(self):
        """Send the message to the Chatbase API."""
        url = "https://chatbase.com/api/message"
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())


class MessageSet(object):
    """Message Set.
    Add messages to a set and send to the Batch API.
    """

    def __init__(self,
                 api_key="",
                 platform="",
                 version="",
                 user_id=""):
        self.api_key = api_key
        self.platform = platform
        self.version = version
        self.user_id = user_id
        self.messages = []

    def append_message(self, message_object):
        """Append a Message object to the set."""
        self.messages.append(message_object)

    def new_message(self,
                    intent="",
                    message="",
                    type=None,
                    not_handled=False,
                    time_stamp=None):
        """Add a message to the internal messages list and return it"""
        self.messages.append(Message(api_key=self.api_key,
                                     platform=self.platform,
                                     version=self.version,
                                     user_id=self.user_id,
                                     intent=intent,
                                     message=message,
                                     type=type,
                                     not_handled=not_handled,
                                     time_stamp=time_stamp))
        return self.messages[-1]

    def to_json(self):
        """Return a JSON version for use with the Chatbase API"""
        return json.dumps({'messages': self.messages},
                          default=lambda i: i.__dict__)

    def send(self):
        """Send the message set to the Chatbase API"""
        url = ("https://chatbase.com/api/messages?api_key=%s" % self.api_key)
        return requests.post(url,
                             data=self.to_json(),
                             headers=Message.get_content_type())
