#!/bin/bash

MAX_CODE_LENGTH=100
MAX_NL_LENGTH=100
BATCH_SIZE=100

curdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
lang=$1

# Create working directory
if [ ! -d "$CODENN_WORK" ]; then
    mkdir -p $CODENN_WORK
fi

# Prepare C# and SQL data
CODE_UNK_THRESHOLD=2
NL_UNK_THRESHOLD=2

python2 buildData.py $lang $MAX_CODE_LENGTH $MAX_NL_LENGTH $CODE_UNK_THRESHOLD $NL_UNK_THRESHOLD

th buildData.lua -language $lang -max_code_length $MAX_CODE_LENGTH -max_nl_length $MAX_NL_LENGTH -batch_size $BATCH_SIZE
