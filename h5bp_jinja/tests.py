# -*- coding: utf-8 -*-
#
# Copyright 2013 Mark Lee
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

from . import parse_template
import os
try:  # Python >= 3
    from io import StringIO
except ImportError:
    from StringIO import StringIO
import sys

if sys.version_info < (2, 7):
    from unittest2 import skipUnless, TestCase
else:
    from unittest import skipUnless, TestCase

if sys.version_info < (3,):
    import codecs
    uopen = lambda f, m='r', **k: codecs.open(f, m, encoding='utf-8', **k)
else:
    uopen = open

BOILERPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'html5-boilerplate')
BOILERPLATE_DIR_EXISTS = os.path.exists(BOILERPLATE_DIR)


class H5BPJinjaTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        if BOILERPLATE_DIR_EXISTS:
            filename = os.path.join(BOILERPLATE_DIR, 'index.html')
            with uopen(filename) as f:
                cls.tpl = StringIO(f.read())

    def tearDown(self):
        self.tpl.seek(0)

    @skipUnless(BOILERPLATE_DIR_EXISTS, 'Could not find boilerplate dir')
    def test_parse_template_basic(self):
        parsed = parse_template(self.tpl)
        self.assertNotEqual(self.tpl.getvalue(), parsed)
        self.assertNotIn('<title></title>', parsed)
        self.assertNotRegex(parsed, u'<!-- (.*?) -->')

    if sys.version_info < (3, 2):

        def assertNotRegex(self, s, re, msg=None):
            return self.assertNotRegexpMatches(s, re, msg)
