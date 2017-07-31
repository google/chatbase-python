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

"""Define the form and function of the chatbase_fields attribute"""


class FacebookID(object):
    """Defines the form of facebook ids."""

    def __init__(self):
        self.id = ""


class FacebookUserMessageContent(object):
    """Defines the form of facebook message content."""

    def __init__(self):
        self.mid = ""
        self.text = ""


class ChatbaseFields(object):
    """Attribute used to store Chatbase params when sending FB messages."""

    def __init__(self):
        self.intent = ""
        self.version = ""
        self.not_handled = False
        self.feedback = False
