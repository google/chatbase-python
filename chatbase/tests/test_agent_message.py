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

import json, os, unittest
from chatbase import *


class TestAgentMessage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAgentMessage, self).__init__(*args, **kwargs)
        # allow long diffs for dictionary comparison outputs
        self.maxDiff = None
        self.inst = FacebookAgentMessage()

    def test_init(self):
        self.assertTrue(isinstance(
            self.inst.request_body, FacebookAgentMessageRequestBody))
        self.assertTrue(isinstance(
            self.inst.response_body, FacebookAgentMessageResponseBody))
        self.assertTrue(isinstance(self.inst.chatbase_fields, ChatbaseFields))

    def test_setting_rec_id(self):
        rec_id = "test-1234"
        i = FacebookAgentMessage()
        i.set_recipient_id(rec_id)
        self.assertEqual(i.request_body.recipient.id, rec_id)
        self.assertEqual(i.response_body.recipient_id, rec_id)

    def test_setting_msg_id(self):
        msg_id = "4567-test"
        i = FacebookAgentMessage()
        i.set_message_id(msg_id)
        self.assertEqual(i.response_body.message_id, msg_id)

    def test_json_encoding(self):
        intent = 'test'
        version = 'test1'
        msg_cnt = 'this is a test.'
        msg_id = '123'
        rec_id = '456'
        i = FacebookAgentMessage(intent=intent, version=version, message=msg_cnt)
        i.set_as_not_handled()
        i.set_as_feedback()
        i.set_recipient_id(rec_id)
        i.set_message_id(msg_id)
        json_out = i.to_json()
        self.assertEqual(json.loads(json_out), {
            'request_body': {
                'timestamp': i.request_body.timestamp,
                'message': {
                    'text': msg_cnt,
                    'mid': msg_id
                },
                'recipient': {'id': rec_id},
            },
            'response_body': {
                'recipient_id': rec_id,
                'message_id': msg_id
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
        i = FacebookAgentMessage(api_key=test_api_key,
                                 message="test-message",
                                 intent="test-library",
                                 version="0.1")
        i.set_recipient_id("123")
        i.set_message_id("456")
        resp = i.send()
        self.assertEqual(resp.status_code, 200)
    
    def test_live_set_send(self):
        test_api_key = os.environ.get('CB_TEST_API_KEY')
        if test_api_key is None:
            print("Warning: Skipping live integration test without test API key.")
            return
        s = FacebookAgentMessageSet(api_key=test_api_key,
                                    version="0.1")
        i = s.new_message()
        i.message = "msg-1"
        i.intent = "int-1"
        i.set_recipient_id("123")
        i.set_message_id("123")
        i = s.new_message()
        i.message = "msg-2"
        i.intent = "int-2"
        i.set_recipient_id("456")
        i.set_message_id("456")
        resp = s.send()
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
