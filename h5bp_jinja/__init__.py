# -*- coding: utf-8 -*-
#
# Copyright 2013, 2014 Mark Lee
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

from __future__ import unicode_literals

from ._compat import _iterify
from itertools import chain
import re

OPTIONAL_SUBS = {
    # Google Analytics ID in config
    'google_analytics': [(re.compile("'UA-XXXXX-X'"),
                          '{{ config.GOOGLE_ANALYTICS_ID }}')],
    # Remove charset meta tag (use charset in Content-Type header instead)
    'no_charset_tag': [(re.compile(' +.*charset="utf-8".*>\n'), '')],
    # Remove IE compat tag (use header instead)
    'no_compat_tag': [(re.compile(' +.*X-UA-Compatible.*>\n'), '')],
    # Make it obvious to Vim that it's a Jinja file
    'vim': [(re.compile('(<!DOCTYPE html>)$'),
             '\\1 {#- vim: set ft=jinja: #}')],
    # webassets support
    'webassets': [
        # CSS
        (re.compile('''\
(?:(\\s+)(<link rel="stylesheet" href=")[^{].*?(">\n))+'''),
         '''
\\1{% assets 'css_all' -%}
\\1\\2{{ ASSET_URL }}\\3\\1{% endassets -%}
'''),
        # JS
        (re.compile('''\
(<body>.*?)(?:(\s+)(<script src=")[^{/].*?("></script>)\n)+''',
                    re.DOTALL),
         '''\\1
\\2{% assets 'js_all' -%}
\\2\\3{{ ASSET_URL }}\\4
\\2{% endassets -%}
'''),
    ],
}

SUBS = [
    # title
    (re.compile('(<(title>))(</\\2)', re.MULTILINE),
     '\\1{% block title %}{% endblock %}\\3'),
    # HTML comments -> Jinja comments
    (re.compile('<!-- (.*?) -->', re.MULTILINE), '{# \\1 #}'),
    # meta description
    (re.compile('(<meta name="description" content=")(">)'),
     '{% if meta_description %}\\1{{ meta_description }}\\2{% endif %}'),
    # content
    (re.compile('<p>.*?</p>'), '{% block content %}{% endblock %}'),
]


def parse_template(tpl_obj, **kwargs):
    tpl = tpl_obj.read()
    subs = SUBS + list(chain(*[s for k, s in _iterify(OPTIONAL_SUBS)
                               if kwargs.get(k)]))
    for regex, repl in subs:
        tpl = regex.sub(repl, tpl)
    return tpl
