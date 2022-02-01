#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2022 F4PGA Authors
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
#
# SPDX-License-Identifier: Apache-2.0

from . import convert

import argparse
import sys
import os


def main(args):
    if not os.path.isfile(args.input_xml):
        print("The {} file does not exist or is a directory"
              .format(args.input_xml))
        exit(2)
    elif not os.path.isdir(os.path.dirname(os.path.realpath(args.output))):
        print("The {} file cannot be created - no such directory"
              .format(args.output))
        exit(2)
    result = convert.vtr_stylize_xml(args.input_xml)
    with open(args.output, 'w') as out:
        out.write(result)
    exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='vtr_xml_utils',
        description="A tool for applying styling changes to the XML files \
                     for Verilog"
    )
    parser.add_argument(
        "input_xml",
        metavar="input.xml",
        type=str,
        help="The path to file that needs to be stylized with XSL files",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="output.xml",
        help="Output filename default 'output.xml'"
    )

    args = parser.parse_args()
    sys.exit(main(args))
