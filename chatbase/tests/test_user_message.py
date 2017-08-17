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

import json, unittest, os
from chatbase import *


class TestUserMessage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUserMessage, self).__init__(*args, **kwargs)
        # allow long diffs for dictionary comparison outputs
        self.maxDiff = None

    def test_init(self):
        api_key = '123-abc'
        intent = '1'
        version = '2'
        message = '3'
        i = FacebookUserMessage(api_key=api_key,
                                intent=intent,
                                version=version,
                                message=message)
        self.assertEqual(i.api_key, api_key)
        self.assertEqual(i.intent, intent)
        self.assertEqual(i.version, version)
        self.assertEqual(i.message, message)

    def test_set_recipient_id(self):
        rec_id = '1234'
        i = FacebookUserMessage()
        i.set_recipient_id(rec_id)
        self.assertEqual(i.recipient.id, rec_id)

    def test_set_sender_id(self):
        snd_id = '5678'
        i = FacebookUserMessage()
        i.set_sender_id(snd_id)
        self.assertEqual(i.sender.id, snd_id)

    def test_set_message_id(self):
        msg_id = 'abc-123'
        i = FacebookUserMessage()
        i.set_message_id(msg_id)
        self.assertEqual(i.fb_message.mid, msg_id)

    def test_to_json(self):
        api_key = '123-abc'
        intent = '1'
        version = '2'
        message = '3'
        rec_id = '1234'
        snd_id = '5678'
        msg_id = 'abc-123'
        i = FacebookUserMessage(
            intent=intent, version=version, message=message)
        i.set_recipient_id(rec_id)
        i.set_sender_id(snd_id)
        i.set_message_id(msg_id)
        i.set_as_not_handled()
        i.set_as_feedback()
        self.assertEqual(json.loads(i.to_json()), {
            'sender': {'id': snd_id},
            'recipient': {'id': rec_id},
            'timestamp': i.timestamp,
            'message': {
                'mid': msg_id,
                'text': message
            },
            'chatbase_fields': {
                'intent': intent,
                'version': version,
                'not_handled': True,
                'feedback': True
            }
        })
    
    def test_live_send(self):
        test_api_key = os.environ.get('CB_TEST_API_KEY')
        if test_api_key is None:
            print("Warning: Skipping live integration test without test API key.")
            return
        i = FacebookUserMessage(api_key=test_api_key,
                                message="test-message",
                                intent="test-library",
                                version="0.1")
        i.set_recipient_id("123")
        i.set_message_id("456")
        i.set_sender_id("789")
        resp = i.send()
        self.assertEqual(resp.status_code, 200)
    
    def test_live_set_send(self):
        test_api_key = os.environ.get('CB_TEST_API_KEY')
        if test_api_key is None:
            print("Warning: Skipping live integration test without test API key.")
            return
        s = FacebookUserMessageSet(api_key=test_api_key,
                                   version="0.1")
        i = s.new_message()
        i.message = "msg-1"
        i.intent = "int-1"
        i.set_recipient_id("123")
        i.set_message_id("123")
        i.set_sender_id("123")
        i = s.new_message()
        i.message = "msg-2"
        i.intent = "int-2"
        i.set_recipient_id("456")
        i.set_message_id("456")
        i.set_sender_id("456")
        resp = s.send()
        self.assertEqual(resp.status_code, 200)
