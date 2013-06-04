#!/usr/bin/env python
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

try:
    import argcomplete
except ImportError:
    argcomplete = None
import argparse
from itertools import chain
import os.path
import re
import sys

DESCRIPTION = 'Converts an HTML5 boilerplate template into a Jinja2 template.'

OPTIONAL_SUBS = {
    # Google Analytics ID in config
    'google_analytics': [(re.compile(ur"'UA-XXXXX-X'"),
                          ur'{{ config.GOOGLE_ANALYTICS_ID }}')],
    # Remove charset meta tag (use charset in Content-Type header instead)
    'no_charset_tag': [(re.compile(ur' +.*charset="utf-8".*>\n'), ur'')],
    # Remove IE compat tag (use header instead)
    'no_compat_tag': [(re.compile(ur' +.*X-UA-Compatible.*>\n'), ur'')],
    # Make it obvious to Vim that it's a Jinja file
    'vim': [(re.compile(ur'(<!DOCTYPE html>)'),
             ur'\1 {#- vim: set ft=jinja: #}')],
    # webassets support
    'webassets': [
        # CSS
        (re.compile(ur'(?:(\s+)(<link rel="stylesheet" href=").*?(">\n))+'),
         ur'''
\1{% assets 'css_all' -%}
\1\2{{ ASSET_URL }}\3\1{% endassets -%}
'''),
        # JS
        (re.compile(u'''\
(<body>.*?)(?:(\s+)(<script src=")[^/].*?("></script>)\n)+''',
                    re.DOTALL),
         ur'''\1
\2{% assets 'js_all' -%}
\2\3{{ ASSET_URL }}\4
\2{% endassets -%}
'''),
    ],
}

SUBS = [
    # title
    (re.compile(ur'(<(title>))(</\2)', re.MULTILINE),
     ur'\1{% block title %}{% endblock %}\3'),
    # HTML comments -> Jinja comments
    (re.compile(ur'<!-- (.*?) -->', re.MULTILINE), ur'{# \1 #}'),
    # meta description
    (re.compile(ur'(<meta name="description" content=")(">)'),
     ur'{% if meta_description %}\1{{ meta_description }}\2{% endif %}'),
    # content
    (re.compile(ur'<p>.*?</p>'), ur'{% block content %}{% endblock %}'),
]

if argcomplete:

    def directory_completer(prefix, **kwargs):
        dirname = os.path.dirname(prefix)
        r_dirname = dirname
        if not dirname:
            dirname = os.getcwd()
        basename = os.path.basename(prefix)
        return (os.path.join(r_dirname, f) for f in os.listdir(dirname)
                if f.startswith(basename) and os.path.isdir(f))


def parse_args(prog, args):
    parser = argparse.ArgumentParser(prog=prog, description=DESCRIPTION)
    arg = parser.add_argument('template_dir', metavar='TEMPLATE_DIR',
                              help='The directory containing the HTML5 '
                                   'Boilerplate git checkout.')
    if argcomplete:
        arg.completer = directory_completer
    parser.add_argument('output_filename', metavar='OUTPUT_FILENAME',
                        help='The path where the Jinja template should be '
                             'written.')
    parser.add_argument('--google-analytics', action='store_true',
                        default=False,
                        help='Replace fake Google Analytics '
                             'ID with Flask config variable.')
    parser.add_argument('--vim', action='store_true', default=False,
                        help='Add vim modeline filetype hint.')
    parser.add_argument('--webassets', action='store_true', default=False,
                        help='Manage CSS/JS assets with webassets.')
    parser.add_argument('--no-charset-tag', action='store_true', default=False,
                        help='Remove the meta charset= tag (you would need to '
                             'use the charset param in the Content-Type '
                             'header instead).')
    parser.add_argument('--no-compat-tag', action='store_true', default=False,
                        help='Remove the X-UA-Compatible meta tag (you would '
                             'need to use the HTTP header instead).')
    if argcomplete:
        argcomplete.autocomplete(parser)
    return parser.parse_args(args)


def parse_template(filename, args):
    tpl = None
    with open(filename) as f:
        tpl = f.read()
    subs = SUBS + list(chain(*[s for k, s in OPTIONAL_SUBS.iteritems()
                               if getattr(args, k)]))
    for regex, repl in subs:
        tpl = regex.sub(repl, tpl)
    return tpl


def main(argv):
    args = parse_args(argv[0], argv[1:])
    template_file = os.path.join(args.template_dir, 'index.html')
    with open(args.output_filename, 'w') as f:
        f.write(parse_template(template_file, args))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
