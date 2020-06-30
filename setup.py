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

"""Setup defines metadata for the python Chatbase Module."""
from setuptools import setup

setup(name='chatbase',
      version='0.2.2',
      description='Python module for interacting with Chatbase APIs',
      url='https://chatbase.com/documentation',
      author='Google Inc.',
      author_email='dightmerc@gmail.com',
      license='Apache-2.0',
      packages=['chatbase'],
      install_requires=['requests', 'aiohttp', 'asyncio'],
      zip_safe=False)
