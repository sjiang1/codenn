
import antlr4
import re
import os.path

import sys
from cpp.CPP14Lexer import CPP14Lexer

def parseCpp(code):
    code = code.replace('\\n', '\n')
    parsedVersion = []
    stream = antlr4.InputStream(code)
    lexer = CPP14Lexer(stream)
    toks = antlr4.CommonTokenStream(lexer)
    toks.fetch(500)
    
    identifiers = {}
    identCount = 0
    for token in toks.tokens:
        if token.type == 126:
            parsedVersion += ["CODE_INTEGER"]
        elif token.type == 133:
            parsedVersion += ["CODE_REAL"]
        elif token.type == 132:
            parsedVersion += ["CODE_CHAR"]
        elif token.type == 134:
            parsedVersion += ["CODE_STRING"]
        elif token.type == 139 or token.type == 140 or token.type == 141 or token.type == 142: # whitespace and comments
            pass
        else:
            parsedVersion += [str(token.text)]

    return parsedVersion

        
