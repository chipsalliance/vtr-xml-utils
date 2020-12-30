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

import itertools
import re

import lxml.etree as ET

# =============================================================================

PORT_SPEC_RE = re.compile(r"(?P<port>[A-Za-z0-9_\-\.]+)(\[(?P<bit>[0-9]+)\])?")

def parse_port_spec(spec):
    """
    Extracts pin index from a port specification. Returns a tuple with
    (port, bit). If there is no bit index bit is set to 0
    """

    # Match
    match = PORT_SPEC_RE.fullmatch(spec)
    assert match is not None, spec

    # No bit index
    if match.group("bit") is None:
        return (match.group("port"), 0)

    # With bit index
    return (match.group("port"), int(match.group("bit")))


def get_port_by_name(parent_xml, name):
    """
    Returns a top-level port object of a mode/pb_type given its name. The name
    may contain bit index which is ignored.
    """

    # Parse
    name, _ = parse_port_spec(name)

    # This is a mode, go to its parent
    if parent_xml.tag == "mode":
        parent_xml = get_pb_parent(parent_xml)

    # Find the port
    for elem in parent_xml:
        if elem.tag in ["input", "output", "clock"]:
            if elem.attrib["name"] == name:
                return elem

    return None

# =============================================================================


def is_leaf_pb(pbtype_xml):
    """
    Checks whether a pb_type is a leaf
    """
    assert pbtype_xml.tag == "pb_type", pb_type_xml.tag

    if "blif_model" in pbtype_xml.attrib:
        return True

    return False


def get_pb_parent(pbtype_xml):
    """
    Returns a parent pb_type of the given element. The parent is always of
    "pb_type" type.
    """

    elem = pbtype_xml.getparent()
    while elem is not None and elem.tag != "pb_type":
        elem = elem.getparent()

    if elem is not None:
        assert elem.tag == "pb_type", elem.tag

    return elem


def get_pb_by_name(parent_xml, name):
    """
    Searches for a pb_type with the given name. Returns either a child or
    the parent. 
    """
    assert parent_xml.tag in ["pb_type", "mode"], parent_xml.tag

    # Check the parent name. If this is a mode then check its parent name
    if parent_xml.tag == "mode":
        parent_pb_xml = get_pb_parent(parent_xml)
        if parent_pb_xml.attrib["name"] == name:
            return parent_pb_xml

    else:
        if parent_xml.attrib["name"] == name:
            return parent_xml

    # Check children
    # FIXME: For now assume no num_pb > 1
    for elem in parent_xml.findall("pb_type"):
        if elem.attrib["name"] == name:
            return elem

    return None


def yield_modes(pbtype_xml):
    """
    Yields all mode elements of a pb_type element. If there are none yield the
    element itself as a default mode.
    """
    assert pbtype_xml.tag == "pb_type", pb_type_xml.tag

    mode_xmls = pbtype_xml.findall("mode")
    if mode_xmls:
        for elem in mode_xmls:
            yield elem

    else:
        yield pbtype_xml

# =============================================================================


def dump_paths(paths, reverse=False):
    """
    Dumps a list of interconnect paths. The list must contain a number of
    lists of tuples (element, port). The element is a libxml ET object
    representing a <direct> of <mux> while port is the input port name.
    """

    for i, path in enumerate(paths):
        names = []

        if reverse:
            p = path[::-1]
        else:
            p = path

        for elem, port in p:
            name = "{}->{}".format(
                port,
                elem.attrib["output"],
            )
            names.append(name)

        line = "{:2d}. ".format(i)
        line += "  ".join([n.ljust(24) for n in names])

        print(line)

# =============================================================================


def walk_up(pbtype_xml, port_xml, bit, paths, curr_path=None):
    """
    Walks up the pb_tree, records all possible paths.
    """
    assert pbtype_xml.tag == "pb_type", pb_type_xml.tag

#    print(" walk_up(): {} {}.{}[{}]".format(
#        pbtype_xml.tag,
#        pbtype_xml.attrib["name"],
#        port_xml.attrib["name"],
#        bit
#    ))

    if curr_path is None:
        curr_path = []

    # This is a leaf pb_type, terminate recursion
    if is_leaf_pb(pbtype_xml):
        paths.append(curr_path)
        return

    port = "{}.{}".format(pbtype_xml.attrib["name"], port_xml.attrib["name"])

    # The port is an input, jump to the parent
    if port_xml.tag in ["input", "clock"]:
        pbtype_xml = get_pb_parent(pbtype_xml)

        # There is no parent, we've reached a top-level pb_type
        if pbtype_xml is None:
            #paths.append(curr_path) # Annotate top-level port
            return

    # Process each mode (there is always at least one implicit)
    for mode_xml in yield_modes(pbtype_xml):

        # Get interconnect
        xml_ic = mode_xml.find("interconnect")
        assert xml_ic is not None, (mode_xml.tag, mode_xml.attrib["name"])

        # Look for elements that reference the given port as a destination
        for conn_xml in xml_ic:

            if conn_xml.tag in ["direct", "mux"]:

                # Parse output port
                out_port_spec = conn_xml.attrib["output"]
                out_port, out_bit = parse_port_spec(out_port_spec)

                # Got a match
                if (out_port, out_bit) == (port, bit):

                    # Parse input port(s)
                    inp_port_specs = conn_xml.attrib["input"].split()
                    for inp_port_spec in inp_port_specs:

                        inp_port, inp_bit = parse_port_spec(inp_port_spec)
                        inp_pb_name, inp_port = inp_port.split(".")

                        # Get pb_type
                        inp_pbtype_xml = get_pb_by_name(mode_xml, inp_pb_name)
                        assert inp_pbtype_xml is not None, (mode_xml.attrib["name"], inp_pb_name)

                        # Get port
                        inp_port_xml = get_port_by_name(inp_pbtype_xml, inp_port)
                        assert inp_port_xml is not None, (inp_pbtype_xml.attrib["name"], inp_port, inp_bit)

                        #print("  walk_up():", conn_xml.tag, conn_xml.attrib, inp_port_spec)

                        # Store the interconnect element
                        branch = list(curr_path)
                        branch.append((conn_xml, inp_port_spec))

                        # Walk upward
                        walk_up(inp_pbtype_xml, inp_port_xml, inp_bit, paths, branch)

            else:
                print("  walk_up(): ERROR: <{}> interconnect not supported yet!".format(conn_xml.tag))


def walk_down(pbtype_xml, port_xml, bit, paths, curr_path=None):
    """
    Walks down the pb_tree, records all possible paths.
    """
    assert pbtype_xml.tag == "pb_type", pb_type_xml.tag

#    print(" walk_down(): {} {}.{}[{}]".format(
#        pbtype_xml.tag,
#        pbtype_xml.attrib["name"],
#        port_xml.attrib["name"],
#        bit
#    ))

    if curr_path is None:
        curr_path = []

    # This is a leaf pb_type
    if is_leaf_pb(pbtype_xml):
        paths.append(curr_path)
        return

    port = "{}.{}".format(pbtype_xml.attrib["name"], port_xml.attrib["name"])

    # The port is an output, jump to the parent
    if port_xml.tag in ["output"]:
        pbtype_xml = get_pb_parent(pbtype_xml)

        # There is no parent, we've reached a top-level pb_type
        if pbtype_xml is None:
            #paths.append(curr_path) # Annotate top-level port
            return

    # Process each mode (there is always at least one implicit)
    for mode_xml in yield_modes(pbtype_xml):

        # Get interconnect
        xml_ic = mode_xml.find("interconnect")
        assert xml_ic is not None, (mode_xml.tag, mode_xml.attrib["name"])

        # Look for elements that reference the given port as a destination
        for conn_xml in xml_ic:

            if conn_xml.tag == "direct":

                # Parse input port
                inp_port_spec = conn_xml.attrib["input"]
                inp_port, inp_bit = parse_port_spec(inp_port_spec)

                # Got a match
                if (inp_port, inp_bit) == (port, bit):

                    # Parse output port
                    out_port_spec = conn_xml.attrib["output"]
                    out_port, out_bit = parse_port_spec(out_port_spec)
                    out_pb_name, out_port = out_port.split(".")

                    # Get pb_type
                    out_pbtype_xml = get_pb_by_name(mode_xml, out_pb_name)
                    assert out_pbtype_xml is not None, (mode_xml.attrib["name"], out_pb_name)

                    # Get port
                    out_port_xml = get_port_by_name(out_pbtype_xml, out_port)
                    assert out_port_xml is not None, (out_pbtype_xml.attrib["name"], out_port, out_bit)

                    #print("  walk_down():", conn_xml.tag, conn_xml.attrib)

                    # Store the interconnect element
                    branch = list(curr_path)
                    branch.append((conn_xml, inp_port_spec))

                    # Walk downward
                    walk_down(out_pbtype_xml, out_port_xml, out_bit, paths, branch)

            else:
                print("  walk_down(): ERROR: <{}> interconnect not supported yet!".format(conn_xml.tag))

# =============================================================================


def add_pack_pattern(path, name):
    """
    Adds pack pattern annotation to all interconnect tags of the path.
    """

    for conn_xml, port in path:
        xml_pp = ET.Element("pack_pattern", {
            "name": name,
            "in_port": port,
            "out_port": conn_xml.attrib["output"]
        })
        conn_xml.append(xml_pp)


def expand_pack_pattern(pp_xml):

    print("Expanding pack pattern '{}'".format(pp_xml.attrib["name"]))

    # Connection
    conn_xml = pp_xml.getparent()
    if conn_xml.tag not in ["direct"]:
        print("ERROR: <{}> interconnect not supported".format(conn_xml.tag))
        return        

    # Remove the original annotation
    conn_xml.remove(pp_xml)

    parent_xml = get_pb_parent(conn_xml)

    paths_up = []
    paths_down = []

    for direction in ["input", "output"]:

        inp_port_spec = conn_xml.attrib["input"]

        # Parse port
        port_spec = conn_xml.attrib[direction]
        port, bit = parse_port_spec(port_spec)
        pb_name, port = port.split(".")

        # Get pb_type
        pbtype_xml = get_pb_by_name(parent_xml, pb_name)
        assert pbtype_xml is not None, (parent_xml.attrib["name"], pb_name)

        # Get port
        port_xml = get_port_by_name(pbtype_xml, port)
        assert port_xml is not None, (parent_xml.attrib["name"], port, bit)

        # Walk
        if direction == "input":
            walk_up(pbtype_xml, port_xml, bit, paths_up, [(conn_xml, inp_port_spec)])
        elif direction == "output":
            walk_down(pbtype_xml, port_xml, bit, paths_down)
        else:
            assert False, direction

    # Join up and down paths to get all possibilities
    paths = []
    for path_up, path_dn in itertools.product(paths_up, paths_down):

        path = path_up[::-1] + path_dn
        paths.append(path)

    # DEBUG
    dump_paths(paths)

    # Annotate
    for i, path in enumerate(paths):

        # FIXME: We don't really want to rename pack patterns (or do we?) so
        # here I'm just adding index suffixes to original names.
        suffix = "" if i == 0 else "_{}".format(i)
        name = pp_xml.attrib["name"] + suffix

        add_pack_pattern(path, name)


def expand_pack_patterns(xml_root):
    """
    This function expands all pack-patterns present in the architecture so that
    they span all possible connections between leaf cells.
    """

    # Identify all pack-patterns
    pp_xmls = [e for e in xml_root.iter() if e.tag == "pack_pattern"]

    # Expand all of them
    for pp_xml in pp_xmls:
        expand_pack_pattern(pp_xml)
