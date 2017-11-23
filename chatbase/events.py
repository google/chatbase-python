# -*- coding: utf-8 -*-

import json
import time
import requests

from abc import abstractmethod


class InvalidEventException(Exception):
    pass


class BaseEvent(object):

    HEADERS = {
        'Content-type': 'application/json',
        'Accept': 'text/plain'
    }

    def __init__(self, api_key=""):
        self.api_key = api_key

    def to_json(self):
        return json.dumps(self, default=lambda i: i.__dict__)

    @abstractmethod
    def send(self):
        pass

    def _send(self, api_url):
        return requests.post(
            api_url,
            data=self.to_json(),
            headers=self.HEADERS
        )


class CustomEventProperty(object):

    FIELDS = [
        'string_value',
        'integer_value',
        'float_value',
        'bool_value'
    ]

    def __init__(
            self,
            property_name,
            string_value=None,
            integer_value=None,
            float_value=None,
            bool_value=None
    ):
        self.property_name = property_name
        self.string_value = string_value
        self.integer_value = integer_value
        self.float_value = float_value
        self.bool_value = bool_value

    def prepare(self):
        for field in self.FIELDS:
            value = getattr(self, field)
            if value is None:
                continue

            return {
                'property_name': self.property_name,
                field: value
            }

        raise InvalidEventException('One of property values must be setted!')


class CustomEvent(BaseEvent):

    def __init__(
            self,
            api_key,
            user_id,
            intent,
            platform,
            version="",
            timestamp_millis=None,
            properties=[]
    ):
        super(CustomEvent, self).__init__(api_key)

        self.user_id = user_id
        self.intent = intent
        self.platform = platform
        self.version = version
        self.timestamp_millis = timestamp_millis or int(round(time.time() * 1e3))
        self.properties = properties

    def add_property(self, some_property):
        if not isinstance(some_property, CustomEventProperty):
            if not isinstance(some_property, dict):
                raise InvalidEventException('Wrong property type!')

            some_property = CustomEventProperty(**some_property)

        self.properties.append(some_property)

    def to_json(self):
        params = self.__dict__.copy()
        params.pop('properties', None)
        return json.dumps(
            dict(
                params,
                **{
                    'properties': [
                        _property.prepare() for _property in self.properties]
                }
            )
        )

    def send(self):
        api_url = 'https://api.chatbase.com/apis/v1/events/insert'
        return self._send(api_url)


class CustomBatchEvents(BaseEvent):

    def __init__(self, api_key, events=[]):
        super(CustomBatchEvents, self).__init__(api_key)

        self.events = events

    def add(self, some_event):
        self.events.append(some_event)

    def send(self):
        api_url = 'https://api.chatbase.com/apis/v1/events/insert_batch'
        return self._send(api_url)


class ClickEvent(BaseEvent):

    def __init__(self, api_key, url, platform, user_id="", version=""):
        super(ClickEvent, self).__init__(api_key)

        self.url = url
        self.platform = platform
        self.user_id = user_id
        self.version = version

    def send(self):
        api_url = 'https://chatbase.com/api/click'
        return self._send(api_url)
