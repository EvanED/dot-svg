#! /usr/bin/env python

import sys
import os
import pydot


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
        return { 'TITLE': node.get_name(), 'HOVER': hover }
    else:
        return None

def hover_from_edge(node):
    hover = node.get('onhover')
    if hover:
        return { 'TITLE': '%s--%s' % (node.get_source(), node.get_destination()),
                 'HOVER': hover }
    else:
        return None


def get_hovers(graph):
    node_hovers = filter(bool, map(hover_from_node, graph.get_node_list()))
    edge_hovers = filter(bool, map(hover_from_edge, graph.get_edge_list()))
    return node_hovers + edge_hovers


def render_objects(dot_graph, template):
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
    
    
