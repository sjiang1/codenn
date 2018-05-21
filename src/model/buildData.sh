#!/bin/bash

MAX_CODE_LENGTH=100
MAX_NL_LENGTH=100
BATCH_SIZE=100

# Create working directory
if [ ! -d "$CODENN_WORK" ]; then
	mkdir $CODENN_WORK
fi


# Prepare C# and SQL data
SQL_UNK_THRESHOLD=3
CSHARP_UNK_THRESHOLD=2
JAVA_UNK_THRESHOLD=2
NL_UNK_THRESHOLD=2

python buildData.py java $MAX_CODE_LENGTH $MAX_NL_LENGTH $JAVA_UNK_THRESHOLD $NL_UNK_THRESHOLD

th buildData.lua -language java -max_code_length $MAX_CODE_LENGTH -max_nl_length $MAX_NL_LENGTH -batch_size $BATCH_SIZE
