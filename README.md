# Python Client for Chatbase
##### A Python library for the [Chatbase API](https://chatbase.com/documentation/ref)

> This is not an official Google product

## Quick Start

```SH
$ pip install git+git://github.com/google/chatbase-python.git
```

## Account Setup
Please see the [Getting Started Section](https://chatbase.com/documentation/quickstart) for information
on configuring one's account and obtaining and API key.

## Using the module

#### One can send individual messages to the Generic and Facebook rest APIs:

Generic:

```PYTHON
from chatbase import Message

msg = Message(api_key="x",
              platform="kik",
              version="0.1",
              user_id="unique-str",
              message="this is a test",
              intent="test")
resp = msg.send()
```

Asynchronous:

```PYTHON
from chatbase import Message

msg = Message(api_key="x",
              platform="kik",
              version="0.1",
              user_id="unique-str",
              message="this is a test",
              intent="test")
resp = msg.sendAsync()
```

Facebook:

```PYTHON
from chatbase import FacebookAgentMessage, FacebookUserMessage

# Agent messages
agnMsg = FacebookAgentMessage(api_key="x", intent="y", version="1", message="a")
# Make sure to set the recipient and message IDs
agnMsg.set_recipient_id("123")
agnMsg.set_message_id("xyz")
resp = agnMsg.send()

# User messages
usrMsg = FacebookUserMessage(api_key="x", intent="y", version="1", message="a")
# Make sure to set the recipient, sender and message IDs
usrMsg.set_recipient_id("123")
usrMsg.set_sender_id("456")
usrMsg.set_message_id("xyz")
resp = usrMsg.send()
```

#### One can send sets of messages as well to the Generic and Facebook rest APIs:

Generic:

```PYTHON
from chatbase import MessageSet

# When we init the message set we can set several properties which will be
# propagated to all message created from the set!
set = MessageSet(api_key="x", platform="x", version="1", user_id="123")
msg = set.new_message(intent="impress", content="goes to 11")
# one can still edit the message normally and these changes will be reflected
# in the containing set
msg.user_id = "shark-sandwich"
# Message type objects can be appended:
msg2 = Message(api_key="x",
              platform="my_platform",
              version="0.1",
              user_id="unique-str",
              message="this is a test",
              intent="test")
set.append_message(msg2)
# Sending the set will send all contained messages to the batch endpoint
resp = set.send()
```

Facebook:

```PYTHON
from chatbase import FacebookAgentMessageSet, FacebookUserMessageSet

# Agent Message Set
agnSet = FacebookAgentMessageSet(api_key="x", version="y")
msg = agnSet.new_message(intent="a", message="b")
# Don't forget to set the message and recipient ids
msg.set_recipient_id("123")
msg.set_message_id("xyz")
resp = agnSet.send()

# User Message Set
usrSet = FacebookUserMessageSet(api_key="a", version="b")
msg = usrSet.new_message(intent="c", message="d")
# Don't for get to set the message, recipient and sender ids
msg.set_recipient_id("123")
msg.set_sender_id("456")
msg.set_message_id("xyz")
resp = usrSet.send()
```

#### Tests
Please place tests in `tests` directory. To run tests, from the repository
root run the following command:

```
$ python -m unittest discover ./chatbase/tests/
```
