#!/bin/bash

if [ ! -f JavaLexer.g4 ]; then
    curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/java/JavaLexer.g4
fi

java -Xmx500M -cp "/home/siyuan_jiang_827/antlr-4.5.3-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python2 JavaLexer.g4
