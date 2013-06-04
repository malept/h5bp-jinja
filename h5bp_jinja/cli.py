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
import os.path

from . import parse_template

DESCRIPTION = 'Converts an HTML5 boilerplate template into a Jinja2 template.'

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


def main(argv):
    args = parse_args(argv[0], argv[1:])
    template_file = os.path.join(args.template_dir, 'index.html')
    with open(template_file) as template:
        with open(args.output_filename, 'w') as f:
            f.write(parse_template(template, **vars(args)))
    return 0
