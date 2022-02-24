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

import lxml.etree as ET
import pkg_resources
import os
from pathlib import Path

from .pack_pattern_expander import expand_pack_patterns


def get_filenames_containing(pattern, rootdir):
    return list(set([str(f) for f in
                     Path(os.path.dirname(rootdir)).rglob(pattern)]))


def vtr_stylize_xml(xmlfilename: str):
    """Applies a set of stylesheet rules to the input model or PB type XML file.
    It also includes the XInclude blocks in the final output.

    Parameters
    ----------
    xmlfilename : str
        The path to the input XML file.

    Returns
    -------
    str
        A string containing formatted XML file, with added parts from the
        XInclude statements in the original XML.
    """
    xslresourcesroot = pkg_resources.resource_filename('vtr_xml_utils',
                                                       'resources')
    xslresourcesroot += '/'
    converters = [
        'identity.xsl',
        'convert-pb_type-attributes.xsl',
        'convert-port-tag.xsl',
        'convert-prefix-port.xsl',
        'pack-patterns.xsl',
        'remove-duplicate-models.xsl',
        'attribute-fixes.xsl',
        'sort-tags.xsl']
    parser = ET.XMLParser(remove_comments=True)
    etdata = ET.parse(xmlfilename, parser)
    etdata.xinclude()
    for c in converters:
        xslt = ET.parse(xslresourcesroot + c, parser)
        transform = ET.XSLT(xslt)
        etdata = transform(etdata)

    # Expand pack-patterns
    expand_pack_patterns(etdata.getroot())

    return '<?xml version="1.0"?>\n' \
           + ET.tostring(etdata, pretty_print=True).decode('utf-8')
