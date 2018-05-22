#!/bin/bash

if [ ! -f JavaLexer.g4 ]; then
    curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/java/JavaLexer.g4
fi

if [ ! -f antlr-4.5.3-complete.jar ]; then
    curl -O http://www.antlr.org/download/antlr-4.5.3-complete.jar
fi

java -Xmx500M -cp "antlr-4.5.3-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python2 JavaLexer.g4
