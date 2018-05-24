#!/bin/bash

LANGUAGE=$1
OUTDIR=$2
GPUIDX=1
BEAMSIZE=10

# Run Training
th main.lua -gpuidx $GPUIDX -language $1 -outdir ${OUTDIR}

# Run prediction
th predict.lua -encoder ${LANGUAGE}.encoder -decoder ${LANGUAGE}.decoder -beamsize $BEAMSIZE -gpuidx $GPUIDX -language ${LANGUAGE}
