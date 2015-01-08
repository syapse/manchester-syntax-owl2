#!/usr/bin/env python
# (c) 2014 Syapse, Inc.
# See LICENSE.txt, MIT License

import sys
import time

from antlr4 import *
from antlr4.InputStream import InputStream
from MOSLexer import MOSLexer
from MOSListener import MOSListener
from MOSParser import MOSParser

class ErrorReporter(MOSListener):
    def visitErrorNode(self, node):
        print node

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

    def visitErrorNode(self, node):
        pass

    def __getattr__(self, name):
        if name.startswith("enter"):
            return self._enter
        if name.startswith("exit"):
            return self._exit
        raise AttributeError(name)

def parse_stream(stream):
    lexer = MOSLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = MOSParser(stream)
    return parser.ontologyDocument()
    

def main(argv):
    parse_stream(InputStream('Ontology: <http://example.org/>'))
    error_reporter = ErrorReporter()
    printer = TreePrinter()
    walker = ParseTreeWalker()
    start = time.time()
    tree = parse_stream(FileStream(argv[1]))
    mid = time.time()
    walker.walk(printer, tree)
    end = time.time()
    walker.walk(error_reporter, tree)
    after_error = time.time()
    sys.stderr.write("Parse time: %s\n" % (mid - start))
    sys.stderr.write("Walk time: %s\n" % (end - mid))
    sys.stderr.write("Error walk time: %s\n" % (after_error - end))
    #print tree.toStringTree()

if __name__ == '__main__':
    main(sys.argv)

