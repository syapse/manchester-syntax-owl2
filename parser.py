#!/usr/bin/env python
# (c) 2014 Syapse, Inc.
# See LICENSE.txt, MIT License

import sys

from antlr4 import *
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
        raise AttributeError(name)


def main(argv):
    input = FileStream(argv[1])
    lexer = MOSLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MOSParser(stream)
    tree = parser.ontologyDocument()
    printer = TreePrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    #print tree.toStringTree()

if __name__ == '__main__':
    main(sys.argv)

