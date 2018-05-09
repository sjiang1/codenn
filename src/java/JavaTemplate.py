
import antlr4
import re
import os.path

import sys
# sys.path.insert(0, '/home/siyuan_jiang_827/codenn-java/src/java/')
from java.JavaLexer import JavaLexer

def parseJava(code):
    code = code.replace('\\n', '\n')
    parsedVersion = []
    stream = antlr4.InputStream(code)
    lexer = JavaLexer(stream)
    toks = antlr4.CommonTokenStream(lexer)
    toks.fetch(500)
    
    identifiers = {}
    identCount = 0
    for token in toks.tokens:
        if token.type == 51 or token.type == 52 or token.type == 53 or token.type ==54 or token.type == 57 or token.type == 60:
            parsedVersion += ["CODE_INTEGER"]
        elif token.type == 55 or token.type == 56:
            parsedVersion += ["CODE_REAL"]
        elif token.type == 58:
            parsedVersion += ["CODE_CHAR"]
        elif token.type == 59:
            parsedVersion += ["CODE_STRING"]
        elif token.type == 109 or token.type == 110 or token.type == 108: # whitespace and comments
            pass
        else:
            parsedVersion += [str(token.text)]

    return parsedVersion

if __name__ == '__main__':
    # testing
    if not os.path.isfile('AllInOne7.java'):
        os.system("curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/java/examples/AllInOne7.java")
    
    with open('AllInOne7.java', 'r') as javafile:
        data=javafile.read()
        print parseJava(data)
        
