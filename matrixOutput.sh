#! /bin/bash

#$ -N matrixOUT
#$ -q bio
#$ -hold_jid matrixAWK

python matrixOutput.py /dfs3/wpoon/wpoon/hpc-concatenation-mapping-master/fastq4R179test 4R179test_matrix