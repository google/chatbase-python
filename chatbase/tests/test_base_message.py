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

import json
import os
import unittest
from chatbase import Message, MessageSet, MessageTypes, InvalidMessageTypeError


class TestMessage(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMessage, self).__init__(*args, **kwargs)
        self.inst = Message()

    def test_init(self):
        self.assertEqual(self.inst.api_key, '')
        self.assertEqual(self.inst.platform, '')
        self.assertEqual(self.inst.message, '')
        self.assertEqual(self.inst.intent, '')
        self.assertEqual(self.inst.version, '')
        self.assertEqual(self.inst.user_id, '')
        self.assertTrue(type(self.inst.time_stamp) is int)
        self.assertEqual(self.inst.type, MessageTypes.USER)
        self.assertFalse(self.inst.not_handled)
        self.assertFalse(self.inst.feedback)

    def test_ts_method(self):
        self.assertTrue(type(Message.get_current_timestamp()) is int)

    def test_type_setting(self):
        # instance the entity in function to eliminate test-case bleeding
        i = Message()
        i.set_as_type_user()
        self.assertEqual(i.type, MessageTypes.USER)
        i.set_as_type_agent()
        self.assertEqual(i.type, MessageTypes.AGENT)

    def test_not_handled_setting(self):
        i = Message()
        i.set_as_not_handled()
        self.assertTrue(i.not_handled)
        i.set_as_handled()
        self.assertFalse(i.not_handled)

    def test_feedback_setting(self):
        i = Message()
        i.set_as_feedback()
        self.assertTrue(i.feedback)
        i.set_as_not_feedback()
        self.assertFalse(i.feedback)

    def test_to_json(self):
        api_key = '1234'
        platform = '1'
        message = '2'
        intent = '3'
        version = '4'
        user_id = '5'
        i = Message(api_key=api_key, platform=platform, message=message,
                    intent=intent, version=version, user_id=user_id)
        i.set_as_not_handled()
        i.set_as_feedback()
        self.assertEqual(json.loads(i.to_json()), {
            'api_key': api_key,
            'platform': platform,
            'message': message,
            'intent': intent,
            'version': version,
            'user_id': user_id,
            'time_stamp': i.time_stamp,
            'type': MessageTypes.USER,  # since we did not set as type agent
            'not_handled': True,
            'feedback': True
        })

    def test_live_send(self):
        test_api_key = os.environ.get('CB_TEST_API_KEY')
        if test_api_key is None:
            print("Warning: Skipping live integration test without test API key.")
            return
        i = Message(api_key=test_api_key,
                    platform="python-lib-test",
                    message="test-message",
                    intent="test-library",
                    version="0.1",
                    user_id="12345")
        resp = i.send()
        self.assertEqual(resp.status_code, 200)
    
    def test_live_set_send(self):
        test_api_key = os.environ.get('CB_TEST_API_KEY')
        if test_api_key is None:
            print("Warning: Skipping live integration test without test API key.")
            return
        s = MessageSet(api_key=test_api_key,
                       platform="python-lib-test",
                       version="0.1",
                       user_id="12345")
        i = s.new_message()
        i.message = "msg-1"
        i.intent = "int-1"
        i = s.new_message()
        i.message = "msg-2"
        i.intent = "int-2"
        resp = s.send()
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
