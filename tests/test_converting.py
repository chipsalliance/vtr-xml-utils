#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020  The SymbiFlow Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier:  ISC

import pytest
from vtr_xml_utils import convert


@pytest.mark.parametrize("testdatafile",
                         convert.get_filenames_containing("*.golden.xml",
                                                          __file__))
def test_converting_and_merging_fpga_architecture(testdatafile):
    inputname = testdatafile.replace('.golden.xml', '.xml')
    result = convert.vtr_stylize_xml(inputname)
    with open(testdatafile) as res:
        golden = res.read()
        assert result == golden
