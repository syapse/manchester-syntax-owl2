#!/usr/bin/env python
# (c) 2014 Syapse, Inc.
# See LICENSE.txt, MIT License

import sys
import time

from antlr4 import *
from antlr4.InputStream import InputStream
from MOSLexer import MOSLexer
from MOSParser import MOSParser

class TreePrinter(object):
    def __init__(self):
        self.level = 0

    def _enter(self, ctx):
        print " " * self.level + type(ctx).__name__[0:-7]
        self.level += 1

    def _exit(self, ctx):
        self.level -= 1
    
    def visitTerminal(self, t):
        print "%s'%s'" % (" " * self.level , t) 

    def __getattr__(self, name):
        if name.startswith("enter"):
            return self._enter
        if name.startswith("exit"):
            return self._exit
        raise AttributeError()

def parse_stream(stream):
    lexer = MOSLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = MOSParser(stream)
    return parser.ontologyDocument()
    

def main(argv):
    parse_stream(InputStream('Ontology: <http://example.org/>'))
    printer = TreePrinter()
    walker = ParseTreeWalker()
    start = time.time()
    tree = parse_stream(FileStream(argv[1]))
    mid = time.time()
    walker.walk(printer, tree)
    end = time.time()
    print "Parse time: %s" % (mid - start)
    print "Walk time: %s" % (end - mid)
    #print tree.toStringTree()

if __name__ == '__main__':
    main(sys.argv)

