#! /usr/bin/env python

import sys
import os
import pydot


_next_id=0
def get_fresh_id():
    """Returns a fresh ID string each time it is called."""
    global _next_id
    this_id = "dot_svg_id_" + str(_next_id)
    _next_id += 1
    return this_id

_seen_ids = set()
def set_id_for_entity(entity):
    """If the given entity (node or edge) has no ID, add a fresh one.

    Also output a warning if the given ID has been seen before.
    """
    global _seen_ids
    this_id = entity.get_id()
    if this_id is None:
        this_id = get_fresh_id()
        entity.set_id(this_id)

    if this_id in _seen_ids:
        sys.stderr.write("%s: WARNING: non-unique ID %s found\n" % (sys.argv[0], this_id))
    _seen_ids.add(this_id)

def add_all_ids(graph):
    for node in graph.get_node_list():
        set_id_for_entity(node)
    for edge in graph.get_edge_list():
        set_id_for_entity(edge)


def translate_line(orig_line, svg, hovers):
    """Returns a line of the template, appropriately translated:

    <!--SVG--> is replaced by the SVG
    <!--HOVER-->... has all hovers put into place

    'hovers' should be a sequence of dictionaries. The 'TITLE' key should be
    the string '<source name>--<target name>' for edges and '<name>' for
    nodes. The 'HOVER' attribute should be the thing to display during a
    hover.
    """
    line = orig_line.strip();
    if line.startswith('<!--'):
        if line == '<!--SVG-->':
            return svg
        elif line.startswith('<!--HOVER-->'):
            return '\n'.join(orig_line.format(**hover) for hover in hovers)
        else:
            print line
            assert false
    else:
        return orig_line


def hover_from_node(node):
    hover = node.get('onhover')
    if hover:
        assert hover[0]=='"'
        assert hover[-1]=='"'
        hover = hover[1:-1]
        return { 'TITLE': node.get_id(), 'HOVER': hover }
    else:
        return None

hover_from_edge = hover_from_node

def get_hovers(graph):
    node_hovers = filter(bool, map(hover_from_node, graph.get_node_list()))
    edge_hovers = filter(bool, map(hover_from_edge, graph.get_edge_list()))
    return node_hovers + edge_hovers


def render_objects(dot_graph, template):
    add_all_ids(dot_graph)
    hovers = get_hovers(dot_graph)
    svg = dot_graph.create(format='svg')
    return (translate_line(orig_line, svg, hovers) for orig_line in template)


def render_files(dot_filename, template_filename, output_filename):
    dot_graph = pydot.graph_from_dot_file(dot_filename)
    with open(template_filename, 'r') as template:
        with open(output_filename, 'w') as output:
            for line in render_objects(dot_graph, template):
                output.write(line)


def main():
    if len(sys.argv) != 4 or sys.argv[1] != '-o':
        print "usage: %s -o output.html input.dot" % sys.argv[0]
        sys.exit(1)

    output_filename = sys.argv[2]
    dot_filename = sys.argv[3]
    template_filename = os.path.join(sys.path[0], '..', 'templates', 'html-embedded')

    print output_filename
    print dot_filename
    print template_filename

    render_files(dot_filename, template_filename, output_filename)


if __name__ == "__main__":
    main()
    
    
