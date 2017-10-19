#! /bin/bash

#$ -N matrixOUT
#$ -q bio
#$ -hold_jid matrixAWK

python matrixOutput.py
