#!/bin/bash

# if [ ! -f CPP14.g4 ]; then
#     curl -O https://raw.githubusercontent.com/antlr/grammars-v4/master/cpp/CPP14.g4
# fi
# replaced the False/True with BoolFalse/BoolTrue in the original .g4

if [ ! -f antlr-4.5.3-complete.jar ]; then
    curl -O http://www.antlr.org/download/antlr-4.5.3-complete.jar
fi

java -Xmx500M -cp "antlr-4.5.3-complete.jar:$CLASSPATH" org.antlr.v4.Tool -Dlanguage=Python2 CPP14.g4
