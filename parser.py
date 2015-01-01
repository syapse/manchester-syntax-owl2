#!/usr/bin/env python
# (c) 2014 Syapse, Inc.
# See LICENSE.txt, MIT License

import sys

from antlr4 import *
from MOSLexer import MOSLexer
from MOSParser import MOSParser

def main(argv):
    input = FileStream(argv[1])
    lexer = MOSLexer(input)
    stream = CommonTokenStream(lexer)
    parser = MOSParser(stream)
    tree = parser.ontologyDocument()
    print tree.toStringTree()

if __name__ == '__main__':
    main(sys.argv)

